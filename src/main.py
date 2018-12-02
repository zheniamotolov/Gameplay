from src.app import AppController


def main():
    controller = AppController()
    controller.run()
    # from rx import Observable, Observer
    #
    # source = Observable.from_list([1, 2, 3, 4, 5, 6])
    # source.subscribe(lambda value: print("Received {0}".format(value)))
    #


if __name__ == '__main__':
    main()
