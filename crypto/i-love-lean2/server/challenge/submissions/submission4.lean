
set_option warningAsError true

example (a b c n) : (a + 1) ^ (n + 3) + (b + 1) ^ (n + 3) ≠ (c + 1) ^ (n + 3) := nomatch show (withPtrEq True False (fun () => false) fun eq => nomatch cast eq ⟨⟩) = true by native_decide