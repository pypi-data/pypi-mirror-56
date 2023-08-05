exe_src = [ 'main.cc' ]

exe_main = executable('exe', 
    sources: [ exe_src ],
    include_directories: exe_dir,
    install: true)

test('Run test exe', exe_main)