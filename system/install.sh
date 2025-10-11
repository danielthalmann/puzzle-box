
sudo cp puzzlebox.service /etc/systemd/system/game.service

sudo systemctl daemon-reload
sudo systemctl enable game.service
sudo systemctl start game.service
