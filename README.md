## For Python Gmail API
https://developers.google.com/gmail/api/quickstart/python

1. Enable app



For signal-cli

need java: https://docs.oracle.com/cd/E19182-01/820-7851/inst_cli_jdk_javahome_t/

Go to Building section of README in signal-cli, clone and build using gradle

deal with libsignal: https://github.com/AsamK/signal-cli/wiki/Provide-native-lib-for-libsignal (you're looking for the dll file, not the so file)

- build the libzkgroup, then use the .dll file in target/release

to make sure JDK in installed

​	java -version

