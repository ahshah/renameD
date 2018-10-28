FROM prod/renamed:18.10.28

RUN rm /usr/local/bin/renameD.py
RUN apt-get install -y python3-pip
RUN pip3 install -U pytest mock pytest-mock pyfakefs
RUN add-apt-repository ppa:neovim-ppa/stable
RUN apt-get update
run apt-get install -y git neovim

RUN git clone https://github.com/ahshah/vimprefs /root/.config/nvim
RUN git clone https://github.com/ahshah/vimprefs /home/user/.config/nvim

