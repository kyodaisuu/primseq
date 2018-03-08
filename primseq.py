#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Primitive sequence analyzer
# written by Fish http://googology.wikia.com/wiki/User:Kyodaisuu
# http://gyafun.jp/ln/primseq.cgi
# MIT License
# Last update: 2018-02-18
# Language: Python 2
#
# When environmental variable SCRIPT_NAME is set, it runs as a CGI program.
# Otherwise it runs as a commandline program.


def main():
    """Show ordinal of a primitive sequence

    Determine if it is commandline or CGI.
    """
    import os
    if os.getenv('SCRIPT_NAME') is None:
        maincl()
    else:
        maincgi()
    return


def maincl():
    """Show ordinal of a primitive sequence

    Invoked from command line.
    """
    # Test some values
    assert primseq('') == 'Empty sequence'
    assert primseq('00000') == '5'
    assert primseq('012') == 'w^w'
    assert primseq('01012') == 'w^w'  # w+w^w is not canonical
    assert primseq('012123') == 'w^(w^w)'  # Another canonical test
    assert primseq('000111') == 'w^3'  # Another canonical test
    assert primseq('123012') == 'w^w+w^w'  # Another canonical test
    assert primseq('0121212') == 'w^(w+w+w)'
    assert primseq('01233451234') == 'w^(w^(w^(w^w))+w^(w^w))'
    assert primseq('0123123') == 'w^(w^w+w^w)'
    assert primseq('012333') == 'w^(w^(w^3))'
    assert primseq('01221') == 'w^(w^2+1)'
    assert primseq('0123122201221') == 'w^(w^w+w^3)+w^(w^2+1)'
    # Change raw_input to input and it works for Python 3
    seq = raw_input('Sequence = ')
    seq = makelist(seq)
    assert seq[0].isdigit()
    seq = standard(seq)
    assert seq[0] == 0
    print(seq)
    print(primseq(seq))
    return


def maincgi():
    """Show ordinal of a primitive sequence

    Running as a CGI program.
    """
    import cgi
    # Comment out for debugging
    # import cgitb
    # cgitb.enable()
    # Write html
    print(r'''Content-Type: text/html

<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Primitive sequence analyzer</title>
  <link rel="stylesheet" type="text/css" href="fish.css">
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.css">
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/contrib/auto-render.min.js"></script>
   <script>$(document).ready(function(){renderMathInElement(document.body,{delimiters: [{left: "$$", right: "$$", display: true},{left: "$", right: "$", display: false}]})});</script>

</head>
<body>
<h1>Primitive sequence analyzer 原始数列解析</h1>

<form action="primseq.cgi" method="post">
  Primitive sequence: <input type="text" name="text" />
  <input type="submit" />
</form>
''')
    footer = r'''<hr>
<p style="text-align: right;"><a
href="http://gyafun.jp/ln/primseq.cgi">Primitive sequence analyzer</a>
(<a href="primseq.txt">Source code</a>)
by <a href="http://googology.wikia.com/wiki/User:Kyodaisuu">Fish</a></p>
</body>
</html>
'''
    # Get form input
    f = cgi.FieldStorage()
    text = f.getfirst('text', '')
    seq = makelist(text)
    if len(seq) > 1 and seq[0].isdigit():
        try:
            seq = standard(seq)
        except Exception:
            print("<p>Error in input</p>")
            print(footer)
            return
        print("</pre>\n<h2>Result</h2>")
        print('<p>Input: {0}</p>'.format(text))
        print('<p>Sequence: {0}</p>'.format(seq))
        ord = primseq(seq)
        ordstr = ord.replace('w', '&omega;')
        ordtex = ord.replace('w', '\omega').replace('(', '{').replace(')', '}')
        print('<p>Ordinal: ${0}$</p>'.format(ordtex))
        print(
            '<p>Text output: {0}</p>'.format(ordstr))
    else:
        print('<p>Input <a href="http://googology.wikia.com/wiki/User_blog:Kyodaisuu/A_program_of_Kirby-Paris_hydra">primitive sequence</a> (<a href="http://ja.googology.wikia.com/wiki/%E5%8E%9F%E5%A7%8B%E6%95%B0%E5%88%97%E6%95%B0">原始数列</a>) with format of:</p>')
        print('<ul><li>012345</li><li>0 1 2 3 4 5</li><li>0,1,2,3,4,5</li></ul>')
        print('<a href="http://ja.googology.wikia.com/wiki/%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%83%96%E3%83%AD%E3%82%B0:Kyodaisuu/%E5%8E%9F%E5%A7%8B%E6%95%B0%E5%88%97%E3%81%AE%E9%A0%86%E5%BA%8F%E6%95%B0%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0">より詳しい説明</a>')
    print(footer)
    return


def makelist(seq):
    """Make list from string

    When comma or space is used, they are used as separators"""
    seq = seq.strip()
    if ',' in seq:
        seq = seq.replace(',', ' ')
    if ' ' in seq:
        seq = seq.split()
    seq = list(seq)
    return seq


def primseq(seq):
    """Convert primitive sequence to ordinal"""
    # Check input sequence
    try:
        if len(seq) == 0:
            return 'Empty sequence'
    except Exception:
        return 'Invalid sequence'
    for i in seq:
        try:
            if int(i) < 0:
                return 'Number should be positive'
        except Exception:
            return 'Invalid number'
    # Convert to standard sequence
    seq = standard(seq)
    right = len(seq)-1
    for i in range(right+1)[::-1]:
        if seq[i] != seq[right]:
            ord = str(right-i)
            break
    if i == 0 and seq[0] == seq[right]:
        return str(right-i+1)
    ord = prim(seq[:i+1], seq[i+1], ord)
    return ord


def prim(seq, num, ord):
    if seq[len(seq)-1] < num:
        if ord == '1':
            ord = 'w'
        else:
            if '+' in ord or '^' in ord:
                ord = 'w^('+ord+')'
            else:
                ord = 'w^'+ord
        if len(seq) == 1:
            return ord
        ord = prim(seq[:len(seq)-1], seq[len(seq)-1], ord)
        return ord
    # A + B
    for i in range(len(seq))[::-1]:
        if seq[i] == num:
            break
    ord = primseq(seq[i:len(seq)]) + '+' + ord
    if i == 0:
        return ord
    ord = prim(seq[:i], seq[i], ord)
    return ord


def standard(seq):
    """Convert sequence to standard expression

    Start from 0: [1,2,3] -> [0,1,2]
    Increment with 1: [0,2,4] -> [0,1,2]"""
    st = stand(seq)
    while len(st) < len(seq):
        seq = st
        st = stand(seq)
    return st


def stand(seq):
    st = []
    offset = int(seq[0])
    nextoffset = offset
    prev = 0
    for i in range(len(seq)):
        offset = nextoffset
        n = int(seq[i])-offset
        if n < 0:
            n = 0
            nextoffset = int(seq[i])
        if n == prev:
            if i == 0:
                st.append(0)
            else:
                st.append(st[i-1])
        if n > prev:
            st.append(st[i-1] + 1)
        if n < prev:
            for j in range(i)[::-1]:
                if n == int(seq[j])-offset:
                    st.append(st[j])
                    break
                if n > int(seq[j])-offset:
                    st.append(st[j]+1)
                    break
        prev = n
    # Check canonical
    # A + B = B when A < B
    i = len(st)-1
    while i > 1:
        i -= 1
        if st[i-1] == st[i]:
            for j in range(i, len(st)):
                if st[j] < st[i]:
                    break
                if st[j] > st[i]:
                    if i == 1:
                        st = st[1:len(st)]
                    else:
                        st = st[:i-1] + st[i:len(st)]
                    break
        if st[i-1] > st[i]:
            for j in range(i)[::-1]:
                if st[j] == st[i]:
                    left = st[j:i]
                    right = st[i:len(st)]
                    # normalize the left part
                    dummy = list(range(left[0]))
                    if dummy + left != list(standard(dummy + left)):
                        return st[:j] + list(standard(dummy + left))[left[0]:]+right
                    found = False
                    equal = True
                    for k in range(len(left)):
                        if len(right) < k+1:
                            continue
                        if left[k] < right[k]:
                            found = True
                        if left[k] > right[k]:
                            equal = False
                            break
                    if equal and found == False and len(left) < len(right) and right[len(left)] > right[0]:
                        found = True
                    if found:
                        if j == 0:
                            return tuple(right)
                        st = st[:j] + right
                        i = j
                    break
    return tuple(st)


if __name__ == '__main__':
    main()
