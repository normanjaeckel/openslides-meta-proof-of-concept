# Proposals

https://jmespath.org/specification.html


## Example

The expression `hasMeetingPerm(<permString>)` is an alias for

    SELECT group.id
    FROM topic
    INNER JOIN meeting
    ON topic.meeting_id == meeting.id
    INNER JOIN group
    ON meeting.id == group.meeting_id
    AND <permString> IN group.permissions


Definitions:

    topic:
      - type: standard
        access:
          organization_management_level: superadmin
          committee_management_level:
          groups: hasMeetingPerm("agenda_item.can_see")
          users:
        fields:
          - id
          - title
          - text
          - sequential_number
          - attachment_ids
          - agenda_item_id
          - list_of_speakers_id
          - tag_ids
          - poll_ids
          - projection_ids
          - meeting_id

    organization:
      - type: global
        access: all
        fields:
          - id
          - name
          - description
          - legal_notice
          - privacy_policy
          - login_text
          - vote_decrypt_public_main_key
          - template_meeting_ids
          - theme_id
          - theme_ids
          - mediafile_ids
          - users_email_sender
          - users_email_replyto
          - users_email_subject
          - users_email_body
          - url

      - type: global
        access: authenticated
        fields:
          - reset_password_verbose_errors
          - enable_electronic_voting
          - enable_chat
          - limit_of_meetings
          - limit_of_users
          - committee_ids
          - active_meeting_ids
          - archived_meeting_ids
          - organization_tag_ids

      - type: standard
        access:
          organization_management_level: can_manage_users
          committee_management_level:
          groups:
          users:
        fields:
          - user_ids

    motion:
      - type: standard
        access:
          organization_management_level: superadmin
          committee_management_level:
          groups: .........
          users:
        fields:
          - id
          - number
          - title  # And some more fields ...

      - type: standard
        access: .....
        fields:
          - text
          - reason

      - type: global
        access: nobody
        fields:
          - number_value
