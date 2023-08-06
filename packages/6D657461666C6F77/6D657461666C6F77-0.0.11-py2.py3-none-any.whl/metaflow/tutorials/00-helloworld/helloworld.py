from metaflow import FlowSpec, step


class HelloFlow(FlowSpec):
    """
    A flow where Metaflow prints 'Hi'.

    Run this flow to validate that Metaflow is installed correctly.

    """
    @step
    def start(self):
        """
        This is the 'start' step. All flows must have a step named 'start' that
        is the first step in the flow.

        """
        print("HelloFlow is starting.")
        self.next(self.hello)

    @step
    def hello(self):
        """
        A step for metaflow to introduce itself.

        """
        print("Hi from:")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"\
              "XXXXXXXXXXXXXXXXXXXXXXXXKKXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"\
              "XXXXx;,;oKXXXXXXk:,,cONk:,,,,,,,,,,,,,,,,,,,,:OKo;,,,:kXXXXOl:,"\
              ",,,,,,,,,lxc,;xXXXXkl:,'''',cdKKo,,oKXXXXOoloOXXXXXd;,l0X\n"\
              "XXN0,   .xXXXXXk.   .kXc   ..........    ....:k:  ..  ;KXXXl.  "\
              "........cl. .dXX0c.  .','.   cO;  ,0NXX0,   cXXXXx.  lXX\n"\
              "XXXo     :KXXXx.    '00,  ,0KKKKKKKKO,  ,OKKK0c  'kc  'ONX0,   "\
              ",OKKKKKKKK:  'ONKc  .o0XXXk'  'k:  'ONXKc    :KXX0,  ,0XX\n"\
              "XNO,     .kNXd.     ,Kx.  ;kkkkkk0XNx.  lXXXXo. .xXo  .xXXk.   "\
              ";kkkkkk0NO'  :KNx.  lXXXXXK;  ,O:  'ONXo.    ,0NKc  .xXXX\n"\
              "XXo  .l'  cKd. .c'  :Kl         .lXXl  .xNXXd.  :kOo.  lXXl    "\
              "      .xNd.  oXXc  .kNXXXNO'  :0c  .kNx. 'c. 'ONd.  lXXXX\n"\
              "NO,  :Kl  .:. .xk.  c0;  .lolloloONK;  ,0NXx.    ..    :XK;   ."\
              "cllllldKXc  .kN0,  ,0NXXXXo  .dXc  .kO' .xO. .k0'  ;0XXXX\n"\
              "Xo  .xNk.    .xNx.  ok.  cXNXXXXXXNk.  cXXO'  ,lllll'  '0O.   c"\
              "XNXXXXXN0'  ;KN0;  ,OXXXKd.  ;0Xl  .l;  lX0, .l:  .kXXXXX\n"\
              "O'  :KNKc   'kXXd. .do   .;,;,;,:ONo  .dN0,  ;0NXXXXl  .kd   .d"\
              "NXXXXXXNx.  .,;,....';;,.   ;OXXo      :0NK;     .oXXXXXX\n"\
              "x,.,kXXXOc:lOXXXx'.;xo..........:OXo..:0Xd'.:OXXXXXXk,.,xo...:0"\
              "NXXXXXXXd'..............';cxKXXXO;...'c0XXXx,...,oKXXXXXX\n"
              "KK0KXXXXXXNXXXXXXK0KXK0KK00KK00KKXXK00KXXKK0KXXXXXXXXK0KXK00KKX"\
              "XXXXXXXXKK00K00000000KKKKXXXXXXXXK000KXXXXXXK000KXXXXXXXX")
        self.next(self.end)

    @step
    def end(self):
        """
        This is the 'end' step. All flows must have an 'end' step, which is the
        last step in the flow.

        """
        print("HelloFlow is all done.")


if __name__ == '__main__':
    HelloFlow()
