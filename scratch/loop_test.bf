++++++++> store 8
< step back into loop_counter
[ loop start
    >+- store 0; temp >
    +- store 0; new_val >

    build_duplicate

    build_loop
    <<< seek_to loop_counter
    [
        > seek_to temp    +
        > seek_to new_val +
        << seek_to loop_counter -
    ]

    move_value temp loop_counter

    > seek_to temp
    [
        < seek_to loop_counter +
        > seek_to temp -
    ]
    > seek_to new_val
    ++++++++++++++++++++++++++++++++++++++++++++++++ add 48 for ascii num
    . print new_val as ascii num
    [-]
    << seek_to loop_counter -
]