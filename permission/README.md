# Proposals

Maybe we can code everything in Python using
https://docs.python.org/3/library/ast.html to parse or dump the code as abstract
syntax tree and then use parsers for the other languages that are required.

Maybe we can code everything in Go using https://pkg.go.dev/go/ast and
https://pkg.go.dev/go/parser the same way.


## Definitions

**Int**, **String**, **Bool**, **Set**, **Map**: Basic data types.

**FQField**: Full-qualified-field identifies a specific field of a specific
model in OpenSlides (regular expression:
`^[a-z][a-z_]*[a-z]/[1-9][0-9]*/[a-z][a-z_]*[a-z]$`).

**Action**: Name of a public OpenSlides backend action.

**ActionVariant**: Name of an action's variant. E. g. a `motion.update` can be
called as manager/admin with a more extensive payload than if it is called as
submitter so the caller can retrieve `asManager` or `asSubmitter` or
`notAllowed` in this case.

**Data**: A map of all cached data the requesting component has access to. The
implementation should accept a pointer or reference, so we do not have to copy
the whole database for each call.


## Interfaces

Each of the following interfaces provide the return value and/or an error value
in case of invalid input (invalid data, non existing user, non existing action
etc.).

### Can see

    canSee = (userIDs : Set Int) (fqFields : Set FQField) (data : Data)
        -> Map Int (Set FQField)

Retrieve a map of requested user IDs to the requested FQFields the respective
user is able to see. We maybe add some syntactic suger interfaces to accept only
one single user or one single FQField or get a boolean as result.

### Who can see

Retrieve a map of all user IDs to the requested FQFields the respective user is
able to see.

    whoCanSee = (fqFields : Set FQField) (data : Data)
        -> Map Int (Set FQField)

This interface might be implemented in another way than just retrieving all
users and calling `canSee` for better performance.

### Can perform

    canPerform = (userID : Int) (action : Action) (data : Data)
        -> Bool

Return true if the user is able to perfom this action regardless of the payload
it sends.

### Which Variant

    whichVariant = (userID : Int) (action : Action) (objectID : Int) (data : Data)
        -> ActionVariant

Returns an action variant (e. g. for `motion.update` it might be
`asManager`,`asSubmitter` or `notAllowed`). If this is called for an action that
has no variants, an error is returned or raised.

### Meeting tab

*Caution: This interface is really client specific, so let's discuss if we
should nevertheless implement it here.*

    meetingTab = (userID : Int) (entry : String) (meetingID : Int) (data : Data)
       -> Bool

Returns true if the user has access to the motion tab, the agenda tab etc. and
its corresponding entry in the main menu in the given meeting.

### Organization tab

*Caution: This interface is really client specific, so let's discuss if we
should nevertheless implement it here.*

    organizationTab = (userID : Int) (entry : String) (data : Data)
       -> Bool

Returns true if the user has access to the respective tab and its corresponding
entry in the main menu on the organization view.
