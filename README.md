# Seal

As part of a recent desire to make anti-markatable software I developed this pointlessly dangerous and sadomasochistic "game"

## INSTALLATION
- `pip install playsound`
- `pip install cryptography`
- `python seal.py`
- Won't work with Windows or Python 2

## GAME CONCEPT 
- As you start the program you will spawn a demanding and tech-savvy seal. 
- The seal needs to be kept happy. Play with it, feed it, and don't make it angry! Your important documents are at stake.
- Communicate and carry out game commands by typing into the seal interaction terminal. 
- When the seal is hungry or annoyed, it will encrypt random files in your computer's `documents` folder. 
- To decrypt encrypted `.sealEncrypted` files you will need to feed your seal tasty fish. Look around your computer for `.tastyfish` files that will spawn after the seal barks at you requesting to be fed. Each `.tastyfish` contains a key that will decrypt one specific file. Go fishing! 
- Feed your seal by placing the tasty fish into your `/FEED_ME` folder and running the feeding command. Your seal will only eat if its feeding area is clean. Depending on how much it's eaten, the seal's crap can take up a lot of space... 
- The more annoyed the seal is, the more frequently it will encrypt your files. 

- You will accrue points based on seal satiety time. These points do nothing and merely serve as a way of showing your friends how much time you've wasted.

- Some helpful commands: `feed, clean, play, stats, exit`

## N.B: 
- The seal only likes to encrypt `'.png', '.jpg', '.pdf', '.txt', '.docx', '.mp3'` and `'.mp4'` files. It does not care for any other file types. Yuk! 
- As you play the game, a `SEALED.seal` file will appear in your game directory. Do not delete this if you have files that you need to decrypt! 
- Do not rename `.sealEncrypted` files or the names of their directories/subdirectories, otherwise you won't be able to decrypt them!
- Exit the game by typing in `exit` and waiting for the program to terminate, otherwise you could risk damaging your data.