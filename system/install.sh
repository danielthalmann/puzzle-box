
sudo cp puzzlebox.service /etc/systemd/system/puzzlebox.service

sudo systemctl daemon-reload
sudo systemctl enable puzzlebox.service
sudo systemctl start puzzlebox.service
