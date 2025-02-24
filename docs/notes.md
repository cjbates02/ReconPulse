## Notes
- Need to refine the detection engine to only detect new devices
- Look into arrango db and other graph databases to store network topology data
- Do we need another database such as prometheus for real time network polls?
- Do we need a detection engine?
- macvendors.com allows up to 1000 requests per day and 2 requests per second for free tier

- In order to scan layer 2 data on external networks, we need another 'scout node' deployed inside of the external network.
    - We would run remote commands on this scout through the 'controller node' to discover layer 2 data.
    - Either via API calls or SSH.
    - API endpoint calls are the better way for scalability and less overhead. Just more work lol.

- Need to test hostname discovery




