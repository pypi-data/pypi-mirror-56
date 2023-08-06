"""
This module is for running a demo server (internal FLE purpose mainly).
To use it, run kalite with --settings=kalite.project.settings.demo or
set then environment variable DJANGO_SETTINGS_MODULE to
'kalite.project.settings.demo'.
"""
from .base import *  # @UnusedWildImport

CENTRAL_SERVER_HOST = "staging.learningequality.org"
SECURESYNC_PROTOCOL = "http"
CENTRAL_SERVER_URL = "%s://%s" % (SECURESYNC_PROTOCOL, CENTRAL_SERVER_HOST)
DEMO_ADMIN_USERNAME = "admin"
DEMO_ADMIN_PASSWORD = "pass"
BACKUP_VIDEO_SOURCE = "http://s3.amazonaws.com/KA-youtube-converted/{youtube_id}.mp4/{youtube_id}.{video_format}"

MIDDLEWARE_CLASSES += (
    'kalite.distributed.demo_middleware.StopAdminAccess',
    'kalite.distributed.demo_middleware.LinkUserManual',
    'kalite.distributed.demo_middleware.ShowAdminLogin',
)
