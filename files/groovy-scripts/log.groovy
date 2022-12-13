import java.util.Arrays;
import java.io.FileInputStream;
import java.io.ByteArrayOutputStream;
import java.awt.EventQueue;
import org.freeplane.plugin.script.proxy.ScriptUtils

/******************************************************************/
def threads = new Thread[Thread.activeCount()]
Thread.currentThread().getThreadGroup().enumerate(threads)

// (@metacoma) sleep interuppted error workaround
//Arrays.stream(threads).forEach(Thread::interrupt)

/******************************************************************/
def name = node.id 
new Thread(() -> { 
  FP.runShell(node.id)
  Thread.sleep(10000)

  def pipeLog = new BufferedReader(new FileReader(new File("/tmp/LOG")));
  while (true) {
    while ((groovy_code_base64 = pipeLog.readLine()) != null) {
        String groovy_code = new String(groovy_code_base64.decodeBase64())
    	println groovy_code
    	String groovy_script = """
import org.freeplane.plugin.script.proxy.ScriptUtils;
def c = ScriptUtils.c();
def node = ScriptUtils.node();
//node.children.each{ it.delete() }
""" + groovy_code;
    println groovy_script
    EventQueue.invokeAndWait(() -> Eval.me(groovy_script))
         
    }
  } 

},name).start()
