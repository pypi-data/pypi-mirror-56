=======
crackie
=======

A simple, silly library to generate combinations.

I wrote this when I forgot part of a password, and decided to try run ~500,000
combinations on the parts I remembered. It worked! Also I decided to publish it
because I had never created a Python package before, so this would learn me
something.


Usage
=====

Say you have forgotten a password, but remember the basics of it. For example,
you remember that it was made up of two words, with some characters altered.
The words could be "verd" and "uberous", and the alterations could be things
like random capital letters, numbers instead of letters, etc. Something that
could be modeled like this::

  variations = [
      {"V", "v"},
      {"E", "e", "3"},
      {"R", "r"},
      {"D", "d"},
      {"", "-", "_", " "},
      {"U", "u"},
      {"B", "b", "8"},
      {"E", "e", "3"},
      {"R", "r"},
      {"O", "o", "0"},
      {"U", "u"},
      {"S", "s", "5", "$"},
      {"", "!", "1"},
  ]

Then you can use this library to generate all possible combinations, such as
"VERDUBEROUS", "V3rd_ubEr0U5" or "v3rd ub3r0U5!".

You'll need a way to test the passwords. For example, if it's a GnuPG passphrase
that you have forgotten, you can use this code to test a single password::

  def try_password(password):
      p = Popen(
          ['gpg', '--pinentry-mode', 'loopback', '--decrypt', '--passphrase', password],
          stdout=PIPE,
          stdin=PIPE
      )
      p.communicate(input)
      p.returncode == 0

And then use the generator ``each_possible_combination`` to do exactly that
(testing each possible combination). Like this::

  from crackie import each_possible_combination

  for candidate in each_possible_combination(variations):
      candidate_string = ''.join(candidate)
      if try_password(candidate_string):
          print("Found the password!", candidate_string);
          break
