FROM python:3.9-windowsservercore-1809

# Required for tensorflow
RUN Invoke-WebRequest 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile vcredist_x64.exe ; \
    Start-Process vcredist_x64.exe -ArgumentList '/install', '/passive', '/norestart' -NoNewWindow -Wait ; \
    Remove-Item vcredist_x64.exe

RUN pip install --no-cache-dir "flask<3" "pillow<11" "numpy<2" tensorflow~=2.13.0

COPY app /app
EXPOSE 80
WORKDIR /app

CMD python -u app.py
