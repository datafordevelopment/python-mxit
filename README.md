# python-mxit

Python wrapper for accessing [Mxit's public APIs](https://dev.mxit.com/docs/restapi)

## Installation

	pip install mxit

## Usage

### [Authentication](https://dev.mxit.com/docs/authentication)

In order to use the Mxit APIs, one needs a *client ID* and *client secret*, which can be obtained by registering your app at [dev.mxit.com](https://dev.mxit.com). With these credentials a client object can be created:

```python
from mxit import Mxit
    
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
```

Certain *Mxit API* calls are publically available, and thus only require app authentication. It is not necessary to specify *scope* when making these calls through this *API wrapper*, since it is already done in the respective functions.

Certain *Mxit API* calls require user authentication. The user would thus need to be redirected to *Mxit's* auth site, where permission will be granted by the user for the requested *scope(s)*. The auth site will then redirect the user back to a specified url with a *code* attached in the query string. This code is then used to obtain the auth token for the following *API* calls. For this flow the url where the auth site needs to redirect back to needs to be specified when instantiating the client:

```python
from mxit import Mxit

client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_url='http://example.org')
client.oauth.get_user_token(SCOPE, RECEIVED_CODE)
```
	
The auth site url to redirect the user to can be obtained with the following call (where *SCOPE* is the required scope(s) for the API calls to be made):

```python
client.oauth.auth_url(SCOPE)
```
	
After the user has granted the desired permissions and the user redirected back the the url as specified, the auth token can be fetched as follows:

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_url='http://example.org')
client.oauth.get_user_token(SCOPE, RECEIVED_CODE)
```
	
From here the client has access to the api calls allowed by the specified *scope*.

### [Messaging API](https://dev.mxit.com/docs/restapi/messaging)

#### [send_message](https://dev.mxit.com/docs/restapi/messaging/post-message-send)

Send a message (from a Mxit app) to a list of Mxit users

*User authentication required*: **NO**

*Required scope*: **message/send**

##### Parameters
* *app_mxit_id* (**required**)
* *target_user_ids* (**required**)
* *message* (**required**)
* *contains_markup* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
	
client.messaging.send_message("example_app_mxit_id", ["mxit_user_id_1", "mxit_user_id_2" ], "This is a test message")
```

#### [send_user_to_user_message](https://dev.mxit.com/docs/restapi/messaging/post-message-send)

Send a message (from a Mxit user) to a list of Mxit users

*User authentication required*: **YES**

*Required scope*: **message/user**

##### Parameters
* *from_user_id* (**required**)
* *target_user_ids* (**required**)
* *message* (**required**)
* *contains_markup* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("message/user", RECEIVED_AUTH_CODE)
client.messaging.send_user_to_user_message("example_mxit_user_id", ["mxit_user_id_1", "mxit_user_id_2" ], "This is a test user to user message")
```

### [User API](https://dev.mxit.com/docs/restapi/user])

#### [get_user_id](https://dev.mxit.com/docs/restapi/user/get-user-lookup-mxitid)

Retrieve the Mxit user's internal "user ID"

*User authentication required*: **NO**

*Required scope*: **profile/public**

##### Parameters
* *mxit_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
	
user_id = client.users.get_user_id("example_mxit_id")
```

#### [get_status](https://dev.mxit.com/docs/restapi/user/get-user-statusmessage)

Retrieve the Mxit user's current status

*User authentication required*: **NO**

*Required scope*: **profile/public**

##### Parameters
* *mxit_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
	
status = client.users.get_status("example_mxit_id")
```

#### [set_status](https://dev.mxit.com/docs/restapi/user/put-user-statusmessage)

Set the Mxit user's status

*User authentication required*: **YES**

*Required scope*: **status/write**

##### Parameters
* *message* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("status/write", RECEIVED_AUTH_CODE)
client.users.set_status("Some awesome status")
```

#### [get_display_name](https://dev.mxit.com/docs/restapi/user/get-user-public-displayname-mxitid)

Retrieve the Mxit user's display name

*User authentication required*: **NO**

*Required scope*: **profile/public**

##### Parameters
* *mxit_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
	
display_name = client.users.get_display_name("example_mxit_id")
```

#### [get_avatar](https://dev.mxit.com/docs/restapi/user/get-user-avatar)

Retrieve the Mxit user's avatar

*User authentication required*: **NO**

*Required scope*: **profile/public**

##### Parameters

If *output_file_path* is set, the file will be saved at that path, otherwise the file data will be returned.

* *mxit_id* (**required**)
* *output_file_path* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
	
client.users.get_avatar("example_mxit_id", output_file_path="/path/to/avatar.png")
data = client.users.get_avatar("example_mxit_id")
```


#### [set_avatar](https://dev.mxit.com/docs/restapi/user/post-user-avatar)

Set the Mxit user's avatar

*User authentication required*: **YES**

*Required scope*: **avatar/write**

##### Parameters

The avatar can either be sent as a bytestream in *data* or as a filepath in *input_file_path*.

* *data* (**optional**)
* *input_file_path* (**optional**)
* *content_type* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("avatar/write", RECEIVED_AUTH_CODE)
client.users.set_avatar(input_file_path="/path/to/avatar.png")
```

#### [delete_avatar](https://dev.mxit.com/docs/restapi/user/delete-user-avatar)

Delete the Mxit user's avatar

*User authentication required*: **YES**

*Required scope*: **avatar/write**

##### Parameters

* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("avatar/write", RECEIVED_AUTH_CODE)
client.users.delete_avatar()
```

#### [get_basic_profile](https://dev.mxit.com/docs/restapi/user/get-user-profile-userid)

Retrieve the Mxit user's basic profile

*User authentication required*: **NO**

*Required scope*: **profile/public**

##### Parameters

* *user_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)
	
basic_profile = client.users.get_basic_profile("example_user_id")
```

#### [get_full_profile](https://dev.mxit.com/docs/restapi/user/get-user-profile)

Retrieve the Mxit user's full profile

*User authentication required*: **YES**

*Required scope*: **profile/private**

##### Parameters

* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("profile/private", RECEIVED_AUTH_CODE)
full_profile = client.users.get_full_profile()
```

#### [update_profile](https://dev.mxit.com/docs/restapi/user/put-user-profile)


Update the Mxit user's profile

*User authentication required*: **YES**

*Required scope*: **profile/write**

##### Parameters

* *about_me* (**optional**)
* *display_name* (**optional**)
* *email* (**optional**)
* *first_name* (**optional**)
* *gender* (**optional**)
* *last_name* (**optional**)
* *mobile_number* (**optional**)
* *relationship_status* (**optional**)
* *title* (**optional**)
* *where_am_i* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("profile/write", RECEIVED_AUTH_CODE)
client.users.update_profile(email="test@test.com", relationship_status=3)
```

#### [add_contact](https://dev.mxit.com/docs/restapi/user/put-user-socialgraph-contact-contact)

Add a contact on Mxit

*User authentication required*: **YES**

*Required scope*: **contact/invite**

##### Parameters

*contact_id* can either be the mxit ID of a service or a Mxit user

* *contact_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("contact/invite", RECEIVED_AUTH_CODE)
client.users.add_contact("example_contact_id")
```


#### [get_contact_list](https://dev.mxit.com/docs/restapi/user/get-user-socialgraph-contactlist)

 Retrieve the Mxit user's full contact list

*User authentication required*: **YES**

*Required scope*: **graph/read**

##### Parameters

*list_filter* options can be found in ``mxit.CONTACT_LIST_FILTER``. The following options are available: **"all", "friends", "apps", "invites", "connections", "rejected", "pending", "deleted", "blocked"**

* *list_filter* (**required**)
* *skip* (**optional**)
* *count* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit, CONTACT_LIST_FILTER
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("graph/read", RECEIVED_AUTH_CODE)
client.users.get_contact_list(CONTACT_LIST_FILTER['all'])
```

#### [get_friend_suggestions](https://dev.mxit.com/docs/restapi/user/get-user-socialgraph-suggestions)

Retrieve the Mxit user's full profile

*User authentication required*: **YES**

*Required scope*: **graph/read**

##### Parameters

* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("graph/read", RECEIVED_AUTH_CODE)
client.users.get_friend_suggestions()
```

#### [get_gallery_folder_list](https://dev.mxit.com/docs/restapi/user/get-user-media)

Retrieve a list of the Mxit user's gallery folders

*User authentication required*: **YES**

*Required scope*: **content/read**

##### Parameters

* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/read", RECEIVED_AUTH_CODE)
client.users.get_gallery_folder_list()
```

#### [create_gallery_folder](https://dev.mxit.com/docs/restapi/user/post-user-media-foldername)

Create a new folder in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/write**

##### Parameters

* *folder_name* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/write", RECEIVED_AUTH_CODE)
client.users.create_gallery_folder("example folder name")
```

#### [delete_gallery_folder](https://dev.mxit.com/docs/restapi/user/delete-user-media-foldername)

Delete a folder in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/write**

##### Parameters

* *folder_name* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/write", RECEIVED_AUTH_CODE)
client.users.delete_gallery_folder("example folder name")
```

#### [rename_gallery_folder](https://dev.mxit.com/docs/restapi/user/put-user-media-foldername)

Rename a folder in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/write**

##### Parameters

* *old_folder_name* (**required**)
* *new_folder_name* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/write", RECEIVED_AUTH_CODE)
client.users.rename_gallery_folder("old example folder name", "new example folder name")
```

#### [delete_gallery_file](https://dev.mxit.com/docs/restapi/user/delete-user-media-file-fileid)

Delete a file in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/write**

##### Parameters

* *file_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/write", RECEIVED_AUTH_CODE)
client.users.delete_gallery_file("example_file_id")
```

#### [rename_gallery_file](https://dev.mxit.com/docs/restapi/user/put-user-media-file-fileid)

Rename a file in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/write**

##### Parameters

* *file_id* (**required**)
* *new_file_name* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/write", RECEIVED_AUTH_CODE)
client.users.rename_gallery_file("example_file_id", "new file name")
```

#### [upload_gallery_file](https://dev.mxit.com/docs/restapi/user/post-user-media-file-foldername)

Upload a file to a folder in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/write**

##### Parameters

The file can either be sent as a bytestream in *data* or as a filepath in *input_file_path*.

* *folder_name* (**required**)
* *file_name* (**required**)
* *data* (**optional**)
* *input_file_path* (**optional**)
* *prevent_share* (**optional**)
* *content_type* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/write", RECEIVED_AUTH_CODE)
client.users.upload_gallery_file("example folder name", "example file name", input_file_path="/path/to/image.png", content_type="image/png")
```

#### [get_gallery_item_list](https://dev.mxit.com/docs/restapi/user/get-user-media-list-foldername)

Get the item listing in a given folder in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/read**

##### Parameters

* *folder_name* (**required**)
* *skip* (**optional**)
* *count* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/read", RECEIVED_AUTH_CODE)
client.users.get_gallery_item_list("example folder name")
```

#### [get_gallery_file](https://dev.mxit.com/docs/restapi/user/get-user-media-content-fileid)

Get a file in the Mxit user's gallery

*User authentication required*: **YES**

*Required scope*: **content/read**

##### Parameters

If *output_file_path* is set, the file will be saved at that path, otherwise the file data will be returned.

* *file_id* (**required**)
* *output_file_path* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET, redirect_uri="http://example.org")
	
client.oauth.get_user_token("content/read", RECEIVED_AUTH_CODE)

client.users.get_gallery_file("example_file_id", output_file_path="/path/to/image.png")
data = client.users.get_avatar("example_file_id")
```

#### upload_file_and_send_file_offer

Upload a file of any type to store and return a FileId once file offer has been sent.

*User authentication required*: **NO**

*Required scope*: **content/send**

##### Parameters

The file can either be sent as a bytestream in *data* or as a filepath in *input_file_path*.

* *file_name* (**required**)
* *user_id* (**required**)
* *data* (**optional**)
* *input_file_path* (**optional**)
* *auto_open* (**optional**)
* *prevent_share* (**optional**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)

user_id = client.users.get_user_id("example_mxit_id")
client.users.upload_file_and_send_file_offer("example_file_name", user_id, input_file_path="/path/to/image.png")
```

#### send_file_offer

Upload a file of any type to store and return a FileId once file offer has been sent.

*User authentication required*: **NO**

*Required scope*: **content/send**

##### Parameters

* *file_id* (**required**)
* *user_id* (**required**)
* *scope* (**optional**)

##### Example

```python
from mxit import Mxit
	
client = Mxit(MXIT_CLIENT_ID, MXIT_CLIENT_SECRET)

user_id = client.users.get_user_id("example_mxit_id")
client.users.send_file_offer("example_file_id", user_id)
```
