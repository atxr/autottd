#Install aws
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

#Install TTD
Invoke-WebRequest https://aka.ms/ttd/download -OutFile ttd.appinstaller
Add-AppxPackage -AppInstallerFile ttd.appinstaller