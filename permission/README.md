# Proposals

Maybe we can code everything in Python using
https://docs.python.org/3/library/ast.html to parse or dump the code as abstract
syntax tree and then use parsers for the other languages that are required.

Maybe we can code everything in Go using https://pkg.go.dev/go/ast and
https://pkg.go.dev/go/parser the same way.

Maybe there is another way?


## Definitions

**Bool**, **Set**, **Map**: Basic data types.

**UserID**: Numeric id of an user.

**ObjectID**: Numeric id of an object like a motion or an agenda item.

**MeetingID**: Numeric id of a meeting.

**FQField**: Full-qualified-field identifies a specific field of a specific
model in OpenSlides (regular expression:
`^[a-z][a-z_]*[a-z]/[1-9][0-9]*/[a-z][a-z_]*[a-z]$`).

**Action**: Name of a public OpenSlides backend action.

**ActionVariant**: Name of an action's variant. E. g. a `motion.update` can be
called as manager/admin with a more extensive payload than if it is called as
submitter so the caller can retrieve `asManager` or `asSubmitter` or
`notAllowed` in this case.

**MeetingMenuEntry**: Name of a menu entry like `agenda`, `motions` or
`settings`.

**OrganizationMenuEntry**: Name a menu entry on the organization view like
`committees`, `accounts` or `files`

**Data**: A map of all cached data the requesting component has access to. The
implementation should accept a pointer or reference, so we do not have to copy
the whole database for each call.

**AccessRecord**: Describes who can see this corresponding field.

The attribute `type` has one of the following values:
  - `nobody` : Nobody can see this field, not even the superuser.
  - `authenticated` : All authenticated users (with login) can see this field.
  - `all` : All user can see this field, even anonymous users.
  - `levelAndGroups` : The `levelAndGroups` attribute is evaluated.

The attribute `levelAndGroups` is a structure with three attributes. Users who fulfill one of them can see the field.

  - `organizationManagementLevel` : One single value. If this is not empty,
    users with this organization management level or higher can see the field.
  - `committeeManagementLevel` : Map of values for some committee ids For every
    given committee, users with this level or higher can see the field.
  - `groups` : Set of group ids. Users in this group can see the field.
  - `userIds` : Some special cases for motion submitters, personal notes and
    email addresses. TODO


## Interfaces

Each of the following interfaces provide the return value and/or an error value
in case of invalid input (invalid data, non existing user, non existing action
etc.).


### Who can see

    whoCanSee = (Set FQField) Data -> Map FQField AccessRecord

TODO ...


### Can see

    canSee = (Set UserID) (Set FQField) Data -> Map UserID (Set FQField)

Retrieve a map of requested user IDs to the requested FQFields the respective
user is able to see. We maybe add some syntactic suger interfaces to accept only
one single user or one single FQField or get a boolean as result (e. g.
`canSeeSingle`).




<!-- Retrieve a map of all user IDs to the requested FQFields the respective user is
able to see.

    whoCanSee = (fqFields : Set FQField) (data : Data)
        -> Map Int (Set FQField)

For better performance this interface might be implemented in another way than
just retrieving all users and calling `canSee` with them. -->


### Can perform

    canPerform = UserID Action Data -> Bool

Return true if the user is able to perfom this action regardless of the payload
it sends.


### Which Variant

    whichVariant = UserID Action ObjectID Data -> ActionVariant

Returns an action variant (e. g. for `motion.update` it might be
`asManager`,`asSubmitter` or `notAllowed`). If this is called for an action that
has no variants, an error is returned or raised.

*Question: Do we have actions with variants that do refer to any other field
than the object ID? E. g. a `motion.update` call depends on the motion ID.
Everything else is retrieved from the dataset.*


### Meeting tab

    meetingTab = UserID MeetingID Data -> Set MeetingMenuEntry

Returns the main menu entries and tabs of a meeting the user has access to.

*Question: This interface is really client specific, so let's discuss if we
should nevertheless implement it here.*


### Organization tab

    organizationTab = UserID Data -> Set OrganizationMenuEntry

Returns the main menu entries and tabs on the organization view the user has
access to.

*Question: This interface is really client specific, so let's discuss if we
should nevertheless implement it here.*
