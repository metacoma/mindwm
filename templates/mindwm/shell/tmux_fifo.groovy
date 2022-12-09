{%- set p = inventory.parameters -%}
#!/usr/bin/env groovy
import java.io.File 

class Example { 
   static void main(String[] args) { 
      def node_id = args[0]
      InputStream Fifo = new FileInputStream("/tmp/tmux-" + node_id + ".fifo");
      int buffer_size = 65536;
      byte[] bytes = new byte[0x10000]; 
      int bytes_read; 
      String tmuxLogContent = ""
      while(1) {
        // wait for stdin

        while ((bytes_read = Fifo.read(bytes, 0, buffer_size)) == -1) {
           print "."
        } 
        String text = new String(bytes, 0, bytes_read)
	tmuxLogContent = tmuxLogContent + text
	text.eachLine { line ->
          if (line.matches(".*@.*")) { 
            File tmuxLog = new File("/tmp/tmux-" + node_id + ".log")
            println tmuxLogContent
            tmuxLog.write tmuxLogContent
            ("{{ p.compiled_dir }}/shell/shell2mindmap.sh " + node_id).execute()
            tmuxLogContent = ""
            println "PROMPT !!!!"
	  }
        }

      }
      
   } 
}
