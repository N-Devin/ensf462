import socket
import time

server_address = ('10.9.183.59', 12000)

# Number of pings to send
num_pings = 10

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize variables for RTT statistics
min_rtt = float('inf')
max_rtt = 0
total_rtt = 0
packets_lost = 0

for sequence_number in range(1, num_pings + 1):
    # Get the current time
    send_time = time.time()

    # Prepare the ping message
    ping_message = f'Ping {sequence_number} {send_time}'

    # Send the ping message to the server
    client_socket.sendto(ping_message.encode(), server_address)

    # Set a timeout for receiving the response (1 second)
    client_socket.settimeout(1)

    try:
        # Receive the response from the server
        response, server_address = client_socket.recvfrom(1024)

        # Calculate the round-trip time (RTT)
        receive_time = time.time()
        rtt = receive_time - send_time

        # Update RTT statistics
        total_rtt += rtt
        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)

        # Print the response message and RTT
        print(f'Response from {server_address}: {response.decode()}')
        print(f'Round-trip time (RTT): {rtt:.6f} seconds')

    except socket.timeout:
        # Handle a timeout (packet loss)
        print(f'Request timed out for sequence number {sequence_number}')
        packets_lost += 1

# Calculate the average RTT
average_rtt = total_rtt / num_pings

# Calculate the packet loss rate
packet_loss_rate = (packets_lost / num_pings) * 100

# Print statistics
print(f'\nPing statistics for {server_address[0]}:')
print(f'Packets: Sent = {num_pings}, Received = {num_pings - packets_lost}, Lost = {packets_lost} ({packet_loss_rate:.2f}% loss)')
print('Approximate round-trip times in milliseconds:')
print(f'Minimum = {min_rtt * 1000:.6f}ms, Maximum = {max_rtt * 1000:.6f}ms, Average = {average_rtt * 1000:.6f}ms')

# Close the socket
client_socket.close()
