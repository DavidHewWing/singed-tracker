from contextlib import redirect_stderr
from getpass import getuser
from unittest import mock
from black import assert_equivalent
import mongomock
from data.guild import Guild
from data.user import User
from mongo.mongo_controller import addGuild, addUserToGuild, deleteGuild, deleteUserInGuild, getGuildById, getUserInGuildByDiscordId

from mongo.mongo_util import guildDoesExist

TEST_VALID_DATA_GUILD_OBJECT = Guild('123', 'andius', [{
         "discordId":"1234",
         "leagueApiId":"2345",
         "summonerName":"BeautifulBussy",
         "discordName":"cyeungster"
      }])
TEST_GUILD_ID_VALID = '123'
TEST_GUILD_ID_INVALID = '890'
TEST_GUILD_NAME = 'andius'
TEST_GUILD_OBJECT = {
   "_id":{
      "oid":"6210209ab3822f44f8d8a685"
   },
   "guildId":"123",
   "name":"andius",
   "users":[
      {
         "discordId":"1234",
         "leagueApiId":"2345",
         "summonerName":"BeautifulBussy",
         "discordName":"cyeungster"
      }
   ]
}

def test_guild_does_exist():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master
   db[TEST_GUILD_ID_VALID].insert_one(TEST_GUILD_OBJECT)
   resultDoesExist = guildDoesExist(mockMongoClient, TEST_GUILD_ID_VALID)
   resultDoesNotExist = guildDoesExist(mockMongoClient, TEST_GUILD_ID_INVALID)
   assert(resultDoesExist)
   assert(not(resultDoesNotExist))

def test_add_guild():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master

   # add when guild doesn't exist
   guild = Guild(TEST_GUILD_ID_VALID, TEST_GUILD_NAME, [])
   resultValid = addGuild(mockMongoClient, guild)
   document = db[TEST_GUILD_ID_VALID].find_one({'name': TEST_GUILD_NAME})
   assert(resultValid)
   assert(guild.name == document['name'])
   assert(guild.users == document['users'])

   # add when already exists
   resultInvalid = addGuild(mockMongoClient, guild)
   assert(not(resultInvalid))

def test_delete_guild():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master
   db[TEST_GUILD_ID_VALID].insert_one(TEST_GUILD_OBJECT)
   resultValid = deleteGuild(mockMongoClient, TEST_GUILD_ID_VALID)
   resultInvalid = deleteGuild(mockMongoClient, TEST_GUILD_ID_INVALID)
   assert(resultValid)
   assert(not(resultInvalid))

def test_get_guild_by_id():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master
   db[TEST_GUILD_ID_VALID].insert_one(TEST_GUILD_OBJECT)
   resultValid, guildResultValid = getGuildById(mockMongoClient, TEST_GUILD_ID_VALID)
   resultInvalid, guildResultInvalid = getGuildById(mockMongoClient, TEST_GUILD_ID_INVALID)
   assert(resultValid)
   assert(guildResultValid.__dict__ == TEST_VALID_DATA_GUILD_OBJECT.__dict__)

def test_add_users_to_guild():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master
   guild = Guild(TEST_GUILD_ID_VALID, TEST_GUILD_NAME, [])
   user = User('1234', '2345', 'BeautifulBussy', 'cyeungster')
   addGuild(mockMongoClient, guild)
   result = addUserToGuild(mockMongoClient, '123', user)
   guild = db['123'].find_one()
   assert(guild['users'][0] == TEST_GUILD_OBJECT['users'][0])
   assert(result)

def test_delete_user_in_guild():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master
   db[TEST_GUILD_ID_VALID].insert_one(TEST_GUILD_OBJECT)
   result = deleteUserInGuild(mockMongoClient, '123', '1234')
   guild = db[TEST_GUILD_ID_VALID].find_one()
   assert([] == guild['users'])
   assert(result)

def test_get_user_in_guild_by_user_id():
   mockMongoClient = mongomock.MongoClient()
   db = mockMongoClient.master
   db[TEST_GUILD_ID_VALID].insert_one(TEST_GUILD_OBJECT)
   userResultValid, resultValid = getUserInGuildByDiscordId(mockMongoClient, '123', '1234')
   deleteUserInGuild(mockMongoClient, '123', '1234')
   userResultInvalid, resultInvalid = getUserInGuildByDiscordId(mockMongoClient, '123', '1234')
   assert(resultValid)
   assert(userResultValid == TEST_GUILD_OBJECT['users'][0])
   assert(userResultInvalid == None)
   assert(not(resultInvalid))
