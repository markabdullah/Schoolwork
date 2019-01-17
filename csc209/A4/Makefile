PORT = 52802
CFLAGS = -Wall -std=gnu99 -g -DPORT=\$(PORT)

hcq_server: hcq_server.o hcq.o socket.o
	gcc $(CFLAGS) -o hcq_server hcq_server.o hcq.o socket.o

%.o: %.c hcq.h socket.h
	gcc $(CFLAGS) -c $<

clean: 
	rm hcq_server *.o
