#named volume oder bindmount ist mir egal.
#
#


# Standard mongo port is 27017. From Outside i change that.
FROM mongo
RUN echo 'My first docker air file.'
#ENV foo=bar
#WORKDIR .
#ist aktuell wahrscheinlich erstmal nicht notwendig. Befehl sollte immer aus dem ordner Repo ausgeführt werdnen.

#COPY conf/mongod.conf TBD
# Wird für das MongoDB hochfahren relevant sein :)

RUN echo 'Your mind just got blown away'