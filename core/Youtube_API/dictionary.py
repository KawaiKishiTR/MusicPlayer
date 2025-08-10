
class sub_api:
    skip_download = {"skip_download": True}
    extract_flat = {"extract_flat": True}
    quiet = {'quiet': True, 'no_warnings': True}
    outtmpl = {'outtmpl': '%(title)s.%(ext)s'}
    write_thumbnail = {'writethumbnail': True}
    opus32 = {'postprocessors': [{'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus','preferredquality': '32'}]}
    opus_format = {'format': 'bestaudio[ext=opus]/bestaudio/best'}
    simulate = {"simulate": True}
    dump_single_json = {"dump_single_json": True}
    playlist_reverse_false = {"extractor_args": {"youtube": ["playlist_reverse=false"]}}
    force_generic_extractor = {"force_generic_extractor": False,}



YT_AUDIO_API = {
    **sub_api.opus_format,
    **sub_api.opus32,
    **sub_api.outtmpl,
    **sub_api.quiet,
}

YT_THUMBNAIL_API = {
    **sub_api.write_thumbnail,
    **sub_api.skip_download,
    **sub_api.quiet,
    **sub_api.outtmpl,
}

YT_INFO_API = {
    **sub_api.outtmpl,
    **sub_api.skip_download,
    **sub_api.quiet,
}

YT_PLAYLIST_PARSER_API = {
    **sub_api.force_generic_extractor,
    **sub_api.playlist_reverse_false,
    **sub_api.dump_single_json,
    **sub_api.simulate,
    **sub_api.skip_download,
    **sub_api.extract_flat,
    **sub_api.quiet,
}

