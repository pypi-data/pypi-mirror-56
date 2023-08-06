from __future__ import print_function
import time
import tarfile
import json
from collections import namedtuple
from itertools import chain

from metaflow.environment import MetaflowEnvironment
from metaflow.exception import MetaflowNotFound,\
                               MetaflowNamespaceMismatch,\
                               MetaflowInternalError

from metaflow.metadata import LocalMetadataProvider, METADATAPROVIDERS
from metaflow.plugins import ENVIRONMENTS

from metaflow.util import cached_property, resolve_identity

from .filecache import FileCache

try:
    # python2
    import cPickle as pickle
except:  # noqa E722
    # python3
    import pickle

Metadata = namedtuple('Metadata', ['name',
                                   'value',
                                   'created_at',
                                   'type',
                                   'task'])

filecache = FileCache()
current_namespace = False

current_metadata = False


def metadata(ms):
    """
    Switch MetaData service.

    This call has a global effect. Selecting the local metadata will,
    for example, not allow access to information stored in remote
    metadata services

    Parameters
    ----------
    ms : string
        Can be a path (selects local metadata), a URL starting with http (selects
        the service metadata at that URL) or explicitly <metadata>@<info> for example
        local@<path> or service@<url>
    """
    global current_metadata
    infos = ms.split('@', 1)
    types = [m.TYPE for m in METADATAPROVIDERS]
    if infos[0] in types:
        current_metadata = [m for m in METADATAPROVIDERS if m.TYPE == infos[0]][0]
        if len(infos) > 1:
            current_metadata.INFO = infos[1]
    else:
        # Deduce from ms; if starts with http, use service or else use local
        if ms.startswith('http'):
            metadata_type = 'service'
        else:
            metadata_type = 'local'
        res = [m for m in METADATAPROVIDERS if m.TYPE == metadata_type]
        if not res:
            print(
                "Cannot find a '%s' metadata provider -- "
                "try specifying one explicitly using <type>@<info>", metadata_type)
            return get_metadata()
        current_metadata = res[0]
        current_metadata.INFO = ms
    return get_metadata()


def get_metadata():
    if current_metadata is False:
        default_metadata()
    return '%s@%s' % (current_metadata.TYPE, current_metadata.INFO)


def default_metadata():
    global current_metadata
    current_metadata = LocalMetadataProvider


def namespace(ns):
    """
    Switch to a namespace specified by the given tag.

    This call has a global effect. No objects outside this namespace
    will be accessible through this module.
    """
    global current_namespace
    current_namespace = ns


def get_namespace():
    """
    Return the current namespace (tag).
    """
    # see a comment about namespace initialization
    # in Metaflow.__init__ below
    if current_namespace is False:
        default_namespace()
    return current_namespace


def default_namespace():
    """
    Set the default namespace.
    """
    global current_namespace
    current_namespace = resolve_identity()


class Metaflow(object):
    """
    The Metaflow class provides an entry point to all objects in
    the Metaflow universe. Use the methods of this class to list
    all flows and webservices.
    """

    def __init__(self):
        # the default namespace is activated lazily at the first object
        # invocation or get_namespace(). The other option of activating
        # the namespace at the import time is problematic, since there
        # may be other modules that alter environment variables etc.
        # which may affect the namescape setting.
        if current_namespace is False:
            default_namespace()
        if current_metadata is False:
            default_metadata()
        self.metadata = current_metadata

    @property
    def flows(self):
        """
        List all flows.

        Returns:
        list: List of `Flow` objects
        """
        return list(self)

    def __iter__(self):
        """
        Iterate over all flows.

        Returns:
        iterator: Iterator over `Flow` objects
        """
        # We do not filter on namespace in the request because
        # filtering on namespace on flows means finding at least one
        # run in this namespace. This is_in_namespace() function
        # does this properly in this case
        all_flows = self.metadata.get_object('root', 'flow')
        for flow in all_flows:
            try:
                v = Flow(_object=flow)
                yield v
            except MetaflowNamespaceMismatch:
                continue

    def __str__(self):
        return 'Metaflow()'

    def __getitem__(self, id):
        return Flow(id)


class MetaflowObject(object):
    _NAME = 'base'
    _CHILD_CLASS = None

    def __init__(self,
                 pathspec=None,
                 _object=None,
                 _parent=None,
                 _namespace_check=True):
        """
        Create a new object of this type given a path to it (`pathspec`).

        To access a Metaflow object, you can either instantiate it directly
        using this method. Alternatively, you can instantiate one of its
        parent objects and use the `Parent[Child]` notation to access the
        child object.

        Here is how to instantiate objects directly:

         - To get a `Flow`, use `Flow('FlowName')`.
         - To get a `Run` of a flow, use `Run('FlowName/RunID')`.
         - To get a `Step` of a run, use `Step('FlowName/RunID/StepName')`.
         - To get a `Task` of a step, use
           `Task('FlowName/RunID/StepName/TaskID')`.
         - To get a `DataArtifact` of a task, use
           `DataArtifact('FlowName/RunID/StepName/TaskID/ArtifactName')`.
        """
        self._metaflow = Metaflow()
        if pathspec:
            ids = pathspec.split('/')

            parents = ids[:-1]
            self.id = ids[-1]
            self._parent = self._create_parents(parents)
            self._object = self._get_object(*ids)
        else:
            self._parent = _parent
            self._object = _object

        if self._NAME in ('flow', 'task'):
            self.id = str(self._object[self._NAME + '_id'])
        elif self._NAME == 'run':
            self.id = str(self._object['run_number'])
        elif self._NAME == 'step':
            self.id = str(self._object['step_name'])
        elif self._NAME == 'artifact':
            self.id = str(self._object['name'])
        else:
            raise MetaflowInternalError(msg="Unknown type: %s" % self._NAME)

        self._created_at = time.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime(self._object['ts_epoch']//1000))

        self._tags = frozenset(chain(self._object.get('system_tags') or [],
                                     self._object.get('tags') or []))

        if _namespace_check and not self.is_in_namespace():
            raise MetaflowNamespaceMismatch(current_namespace)

    def _get_object(self, *path_components):
        result = self._metaflow.metadata.get_object(self._NAME, 'self', None, *path_components)
        if result is None:
            raise MetaflowNotFound("%s does not exist" % self)
        return result

    def _create_parents(self, parents):
        if parents:
            parent = self._metaflow
            for id in parents:
                parent = parent[id]
            return parent
        else:
            return None

    def __iter__(self):
        """
        Iterate over all child objects.
        """
        query_filter = {}
        if current_namespace:
            query_filter = {'any_tags': current_namespace}

        unfiltered_children = self._metaflow.metadata.get_object(
            self._NAME, self._CHILD_CLASS._NAME, query_filter, *self.path_components)

        children = filter(
            lambda x: self._iter_filter(x),
            (self._CHILD_CLASS(_object=obj, _parent=self, _namespace_check=False)
                for obj in unfiltered_children))

        if children:
            return iter(sorted(children, reverse=True, key=lambda x: x.created_at))
        else:
            return iter([])

    def _iter_filter(self, x):
        return True

    def _filtered_children(self, *tags):
        for child in self:
            if all(tag in child.tags for tag in tags):
                yield child

    def is_in_namespace(self):
        if self._NAME == 'flow':
            return any(True for _ in self)
        else:
            return current_namespace is None or\
                   current_namespace in self._tags

    def __str__(self):
        """
        Return a string representation of this object.
        """
        return "%s('%s')" % (self.__class__.__name__, self.pathspec)

    def __repr__(self):
        """
        Return a string representation of this object.
        """
        return str(self)

    def _get_child(self, id):
        result = []
        for p in self.path_components:
            result.append(p)
        result.append(id)
        return self._metaflow.metadata.get_object(
            self._CHILD_CLASS._NAME, 'self', None, *result)

    def __getitem__(self, id):
        """
        Get a child of this object with the given ID.

        Raises `KeyError` if a child with the given ID is not found.
        """
        obj = self._get_child(id)
        if obj:
            return self._CHILD_CLASS(_object=obj, _parent=self)
        else:
            raise KeyError(id)

    def __contains__(self, id):
        """
        Test whether this object has a child with the given ID.

        Return `True` if the child exists, `False` otherwise.
        """
        return bool(self._get_child(id))

    @property
    def tags(self):
        """
        Return the set of tags assigned to this object.
        """
        return self._tags

    @property
    def created_at(self):
        """
        Return a `datetime` object representing the time of creation
        of this object.
        """
        return self._created_at

    @property
    def parent(self):
        """
        Return the parent of this object.
        """
        return self._parent

    @property
    def pathspec(self):
        """
        Return the `pathspec` of this object.

        This path string uniquely identifies this object.
        """
        return '/'.join(self.path_components)

    @property
    def path_components(self):
        """
        Return a list of IDs corresponding to the path to get to this
        object. In other words, this is something like
        [<root>, <great grandparent>, <parent>, <self>]
        """
        def traverse(obj, lst):
            lst.insert(0, obj.id)
            if obj._parent:
                return traverse(obj._parent, lst)
            else:
                return lst
        return traverse(self, [])


class MetaflowData(object):
    """
    A container of data artifacts.

    Individual artifacts are loaded lazily when you access individual
    attributes of this class.
    """

    def __init__(self, artifacts):
        self._artifacts = dict((art.id, art) for art in artifacts)

    def __getattr__(self, name):
        return self._artifacts[name].data

    def __contains__(self, var):
        return var in self._artifacts

    def __str__(self):
        return '< MetaflowData: %s >' % ', '.join(self._artifacts)

    def __repr__(self):
        return str(self)


class MetaflowCode(object):
    """
    Code package that was used to execute a run
    """

    def __init__(self, flow_name, code_package):
        self._flow_name = flow_name
        info = json.loads(code_package)
        self._path = info['location']
        self._ds_type = info['ds_type']
        self._sha = info['sha']
        with filecache.get_data(self._ds_type, self._flow_name, self._sha) as f:
            self._tar = tarfile.TarFile(fileobj=f)
            # The JSON module in Python3 deals with Unicode. Tar gives bytes.
            info_str = self._tar.extractfile('INFO').read().decode('utf-8')
            self._info = json.loads(info_str)
            self._flowspec = self._tar.extractfile(self._info['script']).read()

    @property
    def path(self):
        """
        Return the location of this code package
        """
        return self._path

    @property
    def info(self):
        """
        Return metadata in this code package
        """
        return self._info

    @property
    def flowspec(self):
        """
        Return the source code of the file that includes the FlowSpec executed
        """
        return self._flowspec

    @property
    def tarball(self):
        """
        Return a TarFile object that includes everything in this code package
        """
        return self._tar

    def __str__(self):
        return '< MetaflowCode: %s >' % self._info['script']


class DataArtifact(MetaflowObject):
    """
    The `DataArtifact` class represents a single data artifact and metadata
    related to it.
    """

    _NAME = 'artifact'
    _CHILD_CLASS = None

    @property
    def data(self):
        """
        Return the actual data artifact.
        """
        ds_type = self._object['ds_type']
        sha = self._object['sha']
        with filecache.get_data(ds_type, self.path_components[0], sha) as f:
            obj = pickle.load(f)
            return obj

    # TODO add
    # @property
    # def size(self)

    # TODO add
    # @property
    # def type(self)

    @property
    def sha(self):
        """
        Return the content-based identity (hash) of this data artifact.
        """
        return self._object['sha']

    @property
    def finished_at(self):
        """
        Return a `datetime` object representing the creation time of
        this data artifact.
        """
        return self.created_at


class Task(MetaflowObject):
    """
    The `Task` class represents all tasks in a step.

    Instances of this class contain all data artifacts related to a task.
    """

    _NAME = 'task'
    _CHILD_CLASS = DataArtifact

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def _iter_filter(self, x):
        # exclude private data artifacts
        return x.id[0] != '_'

    @property
    def metadata(self):
        """
        Return a list of metadata events produced by this task.
        """
        all_metadata = self._metaflow.metadata.get_object(
            self._NAME, 'metadata', None, *self.path_components)
        return [Metadata(name=obj.get('field_name'),
                         value=obj.get('value'),
                         created_at=obj.get('ts_epoch'),
                         type=obj.get('type'),
                         task=self) for obj in all_metadata]

    @property
    def metadata_dict(self):
        """
        Return a dictionary of metadata events produced by this task. If
        multiple values exists for a key, the newest value is used.
        """
        # use the newest version of each key, hence sorting
        return {m.name: m.value
                for m in sorted(self.metadata, key=lambda m: m.created_at)}

    @property
    def index(self):
        """
        Return the index of the innermost foreach loop, if this
        task is run inside one or more foreach loops. If the task
        is not inside foreach, return `None`.
        """
        try:
            return self['_foreach_stack'].data[-1].index
        except KeyError:
            return None

    @property
    def data(self):
        """
        Return a container of data artifacts produced by this task.

        You can access data produced by this task as follows:
        ```
        print(task.data.my_var)
        ```
        """
        return MetaflowData(self)

    @property
    def artifacts(self):
        """
        Return a container of `DataArtifact` metadata objects produced
        by this task.
        """
        arts = list(self)
        obj = namedtuple('MetaflowArtifacts', [art.id for art in self])
        return obj._make(arts)

    @property
    def successful(self):
        """
        Return `True` if the task finished successfully, `False` otherwise.
        """
        try:
            return self['_success'].data
        except KeyError:
            return False

    @property
    def finished(self):
        """
        Return `True` if the task has finished, `False` otherwise.
        """
        try:
            return self['_task_ok'].data
        except KeyError:
            return False

    @property
    def exception(self):
        """
        Return the exception that caused this task to fail. Return
        `None` if there is no exception.
        """
        try:
            return self['_exception'].data
        except KeyError:
            return None

    @property
    def finished_at(self):
        """
        Return a `datetime` object representing the finish time of
        this task. Returns `None` if the task has not finished yet.
        """
        try:
            return self['_task_ok'].created_at
        except KeyError:
            return None

    @property
    def runtime_name(self):
        """
        Return the name of the runtime environment where the task was run.
        """
        return self._object['runtime_name']

    @property
    def stdout(self):
        """
        Return the full stdout output of the task.

        The output is returned as a Unicode string.
        """
        logtype = 'stdout'
        return self._load_log(logtype)

    @property
    def stderr(self):
        """
        Return the full stderr output of the task.

        The output is returned as a Unicode string.
        """
        logtype = 'stderr'
        return self._load_log(logtype)

    @cached_property
    def code(self):
        """
        Return a code package, if available, that was used to execute this task.
        """
        code_package = self.metadata_dict.get('code-package')
        if code_package:
            return MetaflowCode(self.path_components[0], code_package)

    @cached_property
    def environment_info(self):
        """
        Return information regarding the environment for this task
        """
        my_code = self.code
        if not my_code:
            return None
        env_type = my_code.info['environment_type']
        if not env_type:
            return None
        env = [m for m in ENVIRONMENTS + [MetaflowEnvironment] if m.TYPE == env_type][0]
        return env.get_client_info(self.path_components[0], self.metadata_dict)

    def _load_log(self, logtype, as_unicode=True):
        ret_val = None
        log_info = self.metadata_dict.get('log_location_%s' % logtype)
        if log_info:
            log_info = json.loads(log_info)
            ds_type = log_info['ds_type']
            attempt = log_info['attempt']
            components = self.path_components
            with filecache.get_log(ds_type, logtype, int(attempt), *components) as f:
                ret_val = f.read()
        if as_unicode and (ret_val is not None):
            return ret_val.decode(encoding='utf8')
        else:
            return ret_val


class Step(MetaflowObject):
    """
    The `Step` class represents all steps in a run.

    Instances of this class contain all tasks related to a step.
    """

    _NAME = 'step'
    _CHILD_CLASS = Task

    @property
    def task(self):
        """
        Return a `Task` object related to this step. This property
        is useful when there is only one task related to this step,
        i.e. when the step is not inside a foreach loop.
        """
        for t in self:
            return t

    def tasks(self, *tags):
        """
        Return an iterator of tasks in this step filtered by the given
        list of tags. All the tags are present in the objects returned.
        """
        return self._filtered_children(*tags)

    @property
    def finished_at(self):
        """
        Return a `datetime` object representing the finish time of
        this step. Returns `None` if the run has not finished yet.

        A step finishes when its last task has finished.
        """
        return max(task.finished_at for task in self)

    @property
    def environment_info(self):
        """
        Return information regarding the environment for this step
        """
        # All tasks have the same environment info so just use the first one
        for t in self:
            return t.environment_info



class Run(MetaflowObject):
    """
    The `Run` class represents all past runs of a flow.

    Instances of this class contain all steps related to a run.
    """

    _NAME = 'run'
    _CHILD_CLASS = Step

    def _iter_filter(self, x):
        # exclude _parameters step
        return x.id[0] != '_'

    def steps(self, *tags):
        """
        Return an iterator of steps in this run filtered by the given
        list of tags. All the tags are present in the objects returned.
        """
        return self._filtered_children(*tags)

    @property
    def code(self):
        """
        Return a code package, if available, that was used to execute this run.
        """
        if 'start' in self:
            return self['start'].task.code

    @property
    def data(self):
        """
        Return a container of data artifacts that were present at the
        end step of the run. If the end step does not exist, return
        `None`.

        This property is a shorthand for `run['end'].task.data`.
        """
        end = self.end_task
        if end:
            return end.data

    @property
    def successful(self):
        """
        Return `True` if this run was successful, `False` otherwise.
        A run is successful if its end task is successful.
        """
        end = self.end_task
        if end:
            return end.successful
        else:
            return False

    @property
    def finished(self):
        """
        Return `True` if this run has finished, `False` otherwise.
        A run finishes when its end task has finished.
        """
        end = self.end_task
        if end:
            return end.finished
        else:
            return False

    @property
    def finished_at(self):
        """
        Return a `datetime` object representing the finish time of
        this run. Returns `None` if the run has not finished yet.
        """
        end = self.end_task
        if end:
            return end.finished_at

    @property
    def end_task(self):
        """
        Return the `Task` object corresponding to the end step of this
        run. Returns `None` if the end task has not finished yet.
        """
        try:
            end_step = self['end']
        except KeyError:
            return None

        for end_task in end_step:
            return end_task


class Flow(MetaflowObject):
    """
    The `Flow` class represents all existing flows with a certain name, i.e.
    classes derived from `FlowSpec`.

    Instances of this class contain all runs related to a flow.
    """

    _NAME = 'flow'
    _CHILD_CLASS = Run

    def __init__(self, *args, **kwargs):
        super(Flow, self).__init__(*args, **kwargs)

    @property
    def latest_run(self):
        """
        Return the latest run of this flow.

        Returns:
        run: A `Run` object if runs exist, `None` otherwise
        """
        for run in self:
            return run

    @property
    def latest_successful_run(self):
        """
        Return the latest successful run of this flow.

        Returns:
        run: A `Run` object if runs exist, `None` otherwise
        """
        for run in self:
            if run.successful:
                return run

    def runs(self, *tags):
        """
        Return an iterator of runs in this flow filtered by the given
        list of tags. All the tags are present in the objects returned.
        """
        return self._filtered_children(*tags)
