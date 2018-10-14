FROM ubuntu:latest
RUN apt-get update && apt-get install -y software-properties-common ca-certificates curl git
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4

RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu


COPY entry.sh /usr/local/bin/entry.sh
RUN chmod 755 /usr/local/bin/entry.sh

COPY bashrc /home/user/.bashrc
COPY bashrc /root/.bashrc
RUN echo "source .bashrc" > /home/user/.bash_profile
RUN echo "source .bashrc" > /root/.bash_profile

RUN git clone https://github.com/ahshah/vimprefs /root/.config/nvim
RUN git clone https://github.com/ahshah/vimprefs /home/user/.config/nvim

RUN add-apt-repository ppa:neovim-ppa/stable
RUN apt-get update
RUN apt-get install -y git neovim python3 python3-pip 
RUN apt-get remove -y python2.7
RUN apt-get autoremove -y
RUN pip3 install -U pytest mock pytest-mock pyfakefs
RUN pip3 install -U inotify
