import helperFunctions.runLinuxCommand as runLinuxCommand
import testClasses.isOnline as isOnline
import sys


if __name__ == '__main__':
    # Domain will be provided as the first command line argument, however for now it is hardcoded for testing purposes
    # domain = sys.argv[1]
    domain = "httpforever.com"
    isOnline.CheckOnlineAndHttp(domain)