==============================
General Array Kalculator (GAK)
==============================

GAK allows for easy and customizable conversion of numbers to
different bases. Here's a crash course in usage::

    from gak import base

    # prints "F"
    print(base(15, 16))

``base()`` takes two arguments: the number being converted, and what
base to convert the number to. An optional third argument is a
custom lookup table for the base conversion that looks as follows::

    #prints "bab"
    print(base(5, 2, {0: "a", 1: "b"}))

It is a dictionary where the key is the number to be converted and
the value is what string the number should become. By default GAK
provides a lookup table up to base16.