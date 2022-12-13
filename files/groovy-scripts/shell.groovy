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
  InputStream Fifo = new FileInputStream("/tmp/freeplane-" + name + ".fifo");
  int buffer_size = 1048576; // # FIXME, buffer too small
  byte[] bytes = new byte[0x100000];
  int bytes_read = -1;
  while(1) {
    while ((bytes_read = Fifo.read(bytes, 0, buffer_size)) == -1) {
//          print "."
      Thread.sleep(1000)
    }
    String text = new String(bytes, 0, bytes_read)
    String groovy_script = """
import org.freeplane.plugin.script.proxy.ScriptUtils;
def c = ScriptUtils.c();
def node = ScriptUtils.node();
//node.children.each{ it.delete() }
""" + text;
    println groovy_script
    EventQueue.invokeAndWait(() -> Eval.me(groovy_script))
  }
},name).start()
