#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>


static unsigned int ADDR;
static unsigned int PORT;

int main()
{
  printf("Starting camera server...\n");
  FILE *picture;
  picture = fopen("/var/image.jpeg", "r");
  int size;
  fseek(picture, 0, SEEK_END); // go to end of the file
  size = ftell(picture);
  fseek(picture, 0, SEEK_SET); // go to begining of file
  char dataSending[size];

  int clintListn = 0, clintConnt = 0;
  struct sockaddr_in ipOfServer;
  clintListn = socket(AF_INET, SOCK_STREAM, 0); // connection oriented TCP protocol

  memset(&ipOfServer, '0', sizeof(ipOfServer)); // fills the struct with zeros
  memset(dataSending, '0', sizeof(dataSending)); // fills the variable with zeros
  ipOfServer.sin_family = AF_INET; // designation of the adress type for communication ipV4
  ipOfServer.sin_addr.s_addr = htonl(ADDR); // convertion to address byte order
  ipOfServer.sin_port = htons(PORT); // convertion to address byte order

  bind(clintListn, (struct sockaddr*)&ipOfServer, sizeof(ipOfServer));
  listen(clintListn, 20);

  while(1)
  {
    printf("Waiting for connection...\n");
    clintConnt = accept(clintListn, (struct sockaddr*)NULL, NULL); // accept connexion with client
    printf("Connection established...\n");

    while(!feof(picture))
    {
      fread(dataSending, 1, sizeof(dataSending), picture); // read picture file into dataSending
      write(clintConnt, dataSending, sizeof(dataSending)); // send dataSending via socket
      printf("Sending image...");
      bzero(dataSending, sizeof(dataSending)); // overwrite picture file with zeros
    }

    close(clintConnt); // close connexion with client
    printf("Closing connexion.");
  }

  return 0;
}
