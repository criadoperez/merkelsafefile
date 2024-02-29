# Merkle Safe File

This application is a simple implementation of a client and server that uses a Merkle tree to verify the integrity of files uploaded to the server.

A user has a large set of potentially small files {F0, F1, …, Fn} and wants to upload them to a server and then delete its local copies. The user wants, however, to later download an arbitrary file from the server and be convinced that the file is correct and is not corrupted in any way (in transport, tampered with by the server, etc.).

This repository implements the client, the server and a Merkle tree to support the above (implementing the Merkle tree rather than using a library).

The client must compute a single Merkle tree root hash and keep it on its disk after uploading the files to the server and deleting its local copies. The client can request the i-th file Fi and a Merkle proof Pi for it from the server. The client uses the proof and compares the resulting root hash with the one it persisted before deleting the files - if they match, file is correct.

## How to run the code

1. Clone this repository

2. Install dependecies

```bash
pip install Flask requests
```

3. Start server
```bash
python3 ./server/server.py
```

4. Run Client

The following example will upload file1.txt and file2.txt to the server, delete the local copies and store the root hash for verification in `root_hast.txt`

```bash
python3 ./client/client.py upload file1.txt file2.txt file3.txt file4.txt
```

Expected output:
```
Node created: cd0df85b1faae4db78bcc5630658361df574068975abcfd4a9d54a6f9451f66b
Node created: 7e16dd2d1a35dbeec595226f9ee16c7f8fc02e4bcbdb355b270fb4504d0bc9db
Node created: e83cbffcb8afc88827c610510cef35be9572b10962c681c0363b22a6945329b8
Node created: 167cc49b3e68809e1eb98528fce1c101473e4febdd5156f78fe43ad4135a0a44
Node created: e45916ce4a0973927db806a3c16f592f6ac9806e71b6f3794aa6231651e95e27
Node created: d539e3d56eebedb91c04541ac0167c6d956101138fcea11ca76e0a17a723fc98
Node created: 4dbac493a233348f6372660d7b3f2b4811082b525133865b76be94d5687d7651
Uploaded file1.txt successfully.
Uploaded file2.txt successfully.
Uploaded file3.txt successfully.
Uploaded file4.txt successfully.
Deleted file1.txt from local storage.
Deleted file2.txt from local storage.
Deleted file3.txt from local storage.
Deleted file4.txt from local storage.
Files uploaded and local copies deleted. Root hash stored for verification.
```

At this point, the server will have the files on the folder `/server_uploaded_files/` and the client will have the root hash for verification. The client can now download the files from the server and verify the integrity of the files.


5. Verify files

```bash
python3 client/client.py verify file1.txt
```

Expected output:
```
Requesting file and proof from the server for file1.txt
File file1.txt has been downloaded successfully.
File hash: cd0df85b1faae4db78bcc5630658361df574068975abcfd4a9d54a6f9451f66b
Proof: ['7e16dd2d1a35dbeec595226f9ee16c7f8fc02e4bcbdb355b270fb4504d0bc9db', 'd539e3d56eebedb91c04541ac0167c6d956101138fcea11ca76e0a17a723fc98']
Stored root hash: 4dbac493a233348f6372660d7b3f2b4811082b525133865b76be94d5687d7651
Intermediate hash after combining with proof element: e45916ce4a0973927db806a3c16f592f6ac9806e71b6f3794aa6231651e95e27
Computed root hash: e45916ce4a0973927db806a3c16f592f6ac9806e71b6f3794aa6231651e95e27
Stored root hash: 4dbac493a233348f6372660d7b3f2b4811082b525133865b76be94d5687d7651
Intermediate hash after combining with proof element: 4dbac493a233348f6372660d7b3f2b4811082b525133865b76be94d5687d7651
Computed root hash: 4dbac493a233348f6372660d7b3f2b4811082b525133865b76be94d5687d7651
Stored root hash: 4dbac493a233348f6372660d7b3f2b4811082b525133865b76be94d5687d7651
The file file1.txt is verified and intact.
```

*If you manually modify the file1.txt on the server you can verify the verification will fail instead.*


## Running with docker

You can also run the server and client with docker. The server will be running on port 5000 and the client will be able to connect to it.

```bash
docker-compose up
```

However currently this will run the server and client on the same machine. For a production scenario you would separate the server from the client as normally they would be in different systems.

## Report on the application

A report on the application can be found in the `report.md` file.