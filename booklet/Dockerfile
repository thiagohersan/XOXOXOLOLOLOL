FROM python:2.7-jessie

ENV BOOK_NAME xoxoxolololol

RUN apt-get update
RUN apt-get install -y libgif4 ghostscript

RUN mkdir -p /tmp/prince && mkdir -p /tmp/book && mkdir -p /opt/book

WORKDIR /tmp/prince/
RUN curl -Os https://www.princexml.com/download/prince_12.3-1_debian8.10_amd64.deb
RUN dpkg -i prince_12.3-1_debian8.10_amd64.deb && apt-get install -f

WORKDIR /tmp/book/
ADD *.html *.css *.py /tmp/book/
ADD texts /tmp/book/texts
ADD images /tmp/book/images
ADD fonts /tmp/book/fonts
RUN python makeBook.py

RUN prince -s style.css ${BOOK_NAME}.html -o ${BOOK_NAME}.pdf
RUN gs -dNOPAUSE -dBATCH -dSAFER -q \
       -dCompatibilityLevel=1.4 \
       -dPDFSETTINGS=/ebook -dUseCIEColor=true \
       -dEmbedAllFonts=true -dSubsetFonts=true \
       -dColorConversionStrategy=/LeaveColorUnchanged \
       -dColorImageDownsampleType=/Bicubic \
       -dColorImageResolution=128 \
       -dGrayImageResolution=128 \
       -sDEVICE=pdfwrite \
       -sOutputFile=${BOOK_NAME}_e.pdf ${BOOK_NAME}.pdf

CMD cp ${BOOK_NAME}*.pdf /opt/book/
