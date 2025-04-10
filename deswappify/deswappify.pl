#!/usr/bin/perl

# ----------------------------------------------------------------------
# 
#   Technique to speed up a subsequent "swapoff" command.
#   Opens /proc/$pid/mem, then seeks and reads.
#
#   Example:
#   perl deswapify.pl
#   swapoff --all
#
#   Forked from:
#   https://gist.github.com/WGH-/91260f6d65db88be2c847053c49be5ae
#
#   Original StackExchange thread:
#   https://unix.stackexchange.com/questions/45673/how-can-swapoff-be-that-slow
#
# ----------------------------------------------------------------------

#use strict;
# Commented out to avoid the following:
# "Bareword "SEEK_SET" not allowed while "strict subs" in use"

my $desc;
my $pid;

sub deswappify {
    my $pid = shift;
    my $fh = undef;
    my $start_addr;
    my $end_addr;

    if(open F, "/proc/$pid/smaps") {

      while(<F>) {

        if(m/^([0-9a-f]+)-([0-9a-f]+) /si){
          $start_addr=hex($1);
          $end_addr=hex($2);
        } elsif( m/^Swap:\s*(\d\d+) *kB/s ){

          if ($fh == undef) {
            if (!open($fh, "< :raw :bytes", "/proc/$pid/mem")) {
              print STDERR "failed to open /proc/$pid/mem\n";
              continue;
            }

            print STDERR "Deswappifying $pid...\n";
          }

          printf STDERR "%x - %x\n", $start_addr, $end_addr;

          seek($fh, $start_addr, SEEK_SET);
          while ($start_addr < $end_addr) {
            read($fh, $_, 4096);
            $start_addr += 4096;
          }
        }
      }

      close $fh if $fh != undef;
    } else {
      print STDERR "failed to open /proc/$pid/smaps\n"
    }
}

for(`ps -e -o pid,args`) {

  if(m/^ *(\d+) *(.{0,40})/) {
    $pid=$1;
    $desc=$2;

    deswappify($pid);
  }
}
