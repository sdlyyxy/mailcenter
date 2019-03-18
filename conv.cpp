#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iconv.h>

int convWord(int code,char* res){
    // printf("code=%x\n",code);
  char *encFrom = "UNICODE//IGNORE";
  char *encTo = "UTF-8";
      /* 获得转换句柄
   *@param encTo 目标编码方式
   *@param encFrom 源编码方式
   *
   * */
  iconv_t cd = iconv_open (encTo, encFrom);
  if (cd == (iconv_t)-1)
  {
      perror ("iconv_open");
  }
    char yxyin[]={char(0xff),char(0xfe),0x06,0x5c,0,0,0};
/* 关闭句柄 */
    // sprintf(yxyin+2,"%x",code);
    yxyin[2]=code%256;
    yxyin[3]=code/256;
    char *yxystart=yxyin;
    size_t tmplen=4;
    char* yxyout=res;
    memset(yxyout,0,10);
     char *yxyoutstart=yxyout;
    size_t yxyoutlen=10;
    // cd = iconv_open ( encFrom,encTo);
    iconv (cd, &yxystart, &tmplen, &yxyoutstart,&yxyoutlen);
    // printf("%s\n",yxyout);
  iconv_close (cd);

}

int main(int argc, char **argv)
{
    char *infilename=argv[1];
    char *outfilename=argv[2];
    FILE *infile=fopen(infilename,"r");
    FILE *outfile=fopen(outfilename,"w");
    int c;
    while((c=fgetc(infile))!=EOF){
        if(c=='&'){
            int nextc=fgetc(infile);
            if(nextc!='#'){
                fputc('&',outfile);
                fputc(nextc,outfile);
                continue;
            }
            int code;
            fscanf(infile,"%d",&code);
            if(code<256){
                
                fprintf(outfile,"&#%d;",code);
                fgetc(infile);
                // fputc(';',outfile);
                continue;
            }
            char buf[10];
            convWord(code,buf);
            fprintf(outfile,"%s",buf);
            fgetc(infile);
        }
        else
        {
            fputc(c,outfile);
        }
        
    }
    fclose(infile);
    fclose(outfile);
    return 0;
}