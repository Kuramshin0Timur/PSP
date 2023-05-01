import psycopg2
import sys
import json

import datetime
import asyncio
from asyncio import coroutine
from os import environ

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

import sqlQueries

tokenToUsernameDict = {}

class MyComponent(ApplicationSession):

    async def onJoin(self, details):

        global tokenToUsernameDict

        print("session joined")

        def usernameExists(username):
            if type(username) is str:
                try:
                    if sqlQueries.userExists(username):
                        print("userExists, True")
                        return "true"
                    else:
                        print("userExists, False")
                        return "false"
                except Exception as e:
                    print("Error, exception:" + str(e))
                    return "error"
            else:
                print("Error \"usernameExists\": username or password are not strings")
                return "error"

        def registerNewUser(username, password, countryCode):
            if type(username) is str and type(password) is str and len(username) >= 6 and len(username) <= 32 and len(
                    password) >= 6 and len(password) <= 40:
                print("----------------------------")
                print("Username: " + username)
                print("Password: " + password)
                print("countryCode " + countryCode)
                print("----------------------------")

                try:
                    if not sqlQueries.userExists(username):
                        result = sqlQueries.registerUser(username, password, countryCode)

                        print("Result:" + str(result))
                        print("User {} with pw \"{}\" has registered sucessfully".format(username, password))
                        return "ok"
                    else:
                        print("User {} already exists.".format(username))
                        return "alreadyExists"
                except Exception as e:
                    print("Error \"registerNewUser\" exception:" + str(e))
                    return "error"
            else:
                print("Error \"registerNewUser\": username or password are not strings")
                return "error"

        def login(username, password):
            global tokenToUsernameDict
            if type(username) is str and type(password) is str:
                try:
                    if sqlQueries.userExists(username):

                        (success, token) = sqlQueries.authenticateUser(username, password)

                        if success is True:
                            tokenToUsernameDict[token] = username
                            print("User {} with pw \"{}\" has logined sucessfully".format(username, password))
                            return ["ok", token]
                        else:
                            print("Wrong auth with username {}.".format(username))
                            return ["wrong", ""]
                    else:
                        print("Username {} does not exists.".format(username))
                        return ["wrong", ""]
                except Exception as e:
                    print("Error \"login\", exception:" + str(e))
                    return ["error", ""]
            else:
                print("Error \"login\": username or password are not strings")
                return ["error", ""]

        await self.register(usernameExists, u'com.usernameExists')
        await self.register(registerNewUser, u'com.registerNewUser')
        await self.register(login, u'com.login')

        def searchRooms(username, query):
            pass

        def searchUsers(username, query):
            return sqlQueries.searchUsername(username, query)

        await self.register(searchUsers, u'com.searchUsers')

        def requestFriendship(username, targetPerson):

            (status, origCaller) = sqlQueries.getFriendshipStatus(username, targetPerson)

            # target person already sent request
            if status == sqlQueries.fRequest and origCaller == targetPerson:
                sqlQueries.setFriendshipStatus(username, targetPerson, sqlQueries.fAccepted)
            else:
                sqlQueries.setFriendshipStatus(username, targetPerson, sqlQueries.fRequest)

            return True

        await self.register(requestFriendship, u'com.requestFriendship')

        def acceptFriendship(username, targetPerson, acceptElseIgnore):

            (status, origCaller) = sqlQueries.getFriendshipStatus(username, targetPerson)

            if status == sqlQueries.fRequest and origCaller == targetPerson:
                sqlQueries.setFriendshipStatus(username, targetPerson, sqlQueries.fRequest)
                return True
            else:
                return False

        await self.register(acceptFriendship, u'com.acceptFriendship')

        def getAllFriends(username):
            return sqlQueries.getAllFriends(username)

        await self.register(getAllFriends, u'com.getAllFriends')

        def sendMessage(chatroomName, username, text, timestamp):
            return False

        def getMessages(chatroomName, username, from_timestamp, to_timestamp):
            pass

        def friendshipToRoomName(friend1, friend2):
            arr = [friend1, friend2]
            arr.sort()
            return arr[0] + "____" + arr[1]

        def createRoom(username, roomName):
            pass

        def joinRoom(username, roomName):
            pass

        def searchPublicRoom(username, query):
            pass

        def inviteToRoom(username, roomName, targetPerson):
            pass

        sqlQueries.setFriendshipStatus("kmetkmet", "drekdrek", "Accepted")
        print(str(sqlQueries.getAllFriends("kmetkmet")))


if __name__ == '__main__':

    print("Connecting to database")

    try:
        sqlQueries.connectDatabase()

    except Exception as e:
        print(e)

    print("Running server component.")

    try:
        runner = ApplicationRunner(url=u"ws://127.0.0.1:8080/ws", realm=u"realm1")
        runner.run(MyComponent)

    except Exceptio(n as e:printe)