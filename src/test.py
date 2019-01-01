import commandprocessing

def main():
    cp = commandprocessing.CommandProcessor("../Example/config.txt")
    print(cp.parse('TURN ON LIGHT'))
    print(cp.parse('TURN Fan OFF'))

if __name__ == '__main__':
    main()
