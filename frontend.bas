10 print chr$(147)
12 poke 53280,1 : poke 53281,1
30 print "      commodore 64 llm rag client"
36 print chr$(17);
37 print chr$(17);
38 print "ask the c64 user guide for help"
1100 open2,2,4,chr$(8)+chr$(0)
1200 get#2,s$
1300 get k$
1400 poke 204,0
1500 if k$<>"" then print#2,k$;:print k$;
1600 get#2,s$
1700 if s$<>"" then print s$;
1800 if (peek(673)and1) then 245
1900 goto 1300
2000 close 2:end