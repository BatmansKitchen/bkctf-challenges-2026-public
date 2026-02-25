set_option warningAsError true

def mem_effecient_mod_exp (b e m c : Nat) : Nat :=
    if e > 0 then
      mem_effecient_mod_exp b (e - 1) m ((b * c) % m)
    else
      c % m

theorem it_works (b e m : Nat) : mem_effecient_mod_exp b e m 1 = (b ^ e) % m :=
