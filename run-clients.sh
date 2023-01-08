for port in {50001..50007}; do
  nohup python3 client.py --client-port $port --server-port 55555 &
done