exe_src = [ 'main.c' ]

exe_main = executable('exe', 
    sources: [ exe_src ],
    include_directories: exe_dir)

benchmark('Run benchmark exe', exe_main)
test('Run test exe', exe_main)
