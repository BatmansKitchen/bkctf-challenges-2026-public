

set_option warningAsError true

def Prime (p : Nat) := ∀ x : Nat, x > 0 → x < p → Nat.gcd x p = 1

def egcd (a b : Nat) : Nat × Nat × Nat :=
  if _h : b = 0 then (a, 1, 0) else
  let (g, x, y) := egcd b (a % b)
  (g, y, x - (Nat.div a b) * y)
  termination_by b decreasing_by
    exact Nat.mod_lt a (Nat.pos_of_ne_zero _h)

def mod_inverse (a m : Nat) (_h : Nat.gcd a m = 1) :=
  let (_, x, _) := egcd a m
  x % m

def encrypt_rsa
  (e p q m : Nat)
  (_p_prime : Prime p)
  (_q_prime : Prime q)
  (_phi_coprime : Nat.gcd e ((p - 1) * (q - 1)) = 1)
  (_msg_bound : m < p * q) : Nat := (m ^ e) % (p * q)


-- example : Nat := encrypt_rsa 3 3 3 3 (fun x hpos hlt => by match x with | 1 => decide | 2 => decide) (fun x hpos hlt => by match x with | 1 => decide | 2 => decide) (by decide) (by decide)


def decrypt_rsa
  (e p q c : Nat)
  (_p_prime : Prime p)
  (_q_prime : Prime q)
  (_phi_coprime : Nat.gcd e ((p - 1) * (q - 1)) = 1)
  (gcd_eq_one : Nat.gcd e ((p - 1) * (q - 1) / Nat.gcd (p - 1) (q - 1)) = 1):=
  (c ^ (mod_inverse e ((p - 1) * (q - 1) / Nat.gcd (p - 1) (q - 1)) gcd_eq_one)) % (p * q)



theorem mul_mod (a b m : Nat) : (a * b) % m = ((a % m) * (b % m)) % m := by
  exact Nat.mul_mod a b m


def mem_effecient_mod_exp (b e m c : Nat) : Nat :=
    if e > 0 then
      mem_effecient_mod_exp b (e - 1) m ((b * c) % m)
    else
      c % m

theorem it_works (b e m : Nat) : mem_effecient_mod_exp b e m 1 = (b ^ e) % m := by
  have h : ∀ c : Nat, mem_effecient_mod_exp b e m c = ((b ^ e) * c) % m := by
    induction e with
    | zero =>
      unfold mem_effecient_mod_exp
      simp
    | succ a ih =>
      intro c
      unfold mem_effecient_mod_exp
      simp
      rw[ih (b * c % m)]
      rw[Nat.pow_add]
      simp
      rw[Nat.mul_assoc, mul_mod (b ^ a) (b * c) m, mul_mod b c m, mul_mod (b^a) (b % m * (c % m) % m) m, Nat.mod_mod (b % m * (c % m)) m]
  rw[h 1, Nat.mul_one]




theorem gcd_works : ∀ a b n : Nat, n ∣ a → n ∣ b → a ≠ 0 → b ≠ 0 → n ≤ Nat.gcd a b := by
  intro a
  induction a with
  | zero => simp
  | succ p ih =>
    intro b
    induction b with
    | zero => simp
    | succ q ih2 =>
      intro n
      induction n with
      | zero => simp
      | succ m ih3 =>
        intro h1 h2 h3 h4





  induction n with
  | zero => simp
  | succ m ih =>
    intro a b h1 h2 h3 h4


  unfold Dvd.dvd at h1 h2
  unfold Nat.instDvd at h1 h2
  simp at h1 h2
  cases h1 with
  | intro x hx =>
    cases h2 with
    | intro y hy =>
      induction n with
      | zero => simp_all
      | succ m ih =>
        simp_all






theorem we_can_decrypt
  (e p q m : Nat)
  (p_prime : Prime p)
  (q_prime : Prime q)
  (phi_coprime : Nat.gcd e ((p - 1) * (q - 1)) = 1)
  (msg_bound : m < p * q)
  (gcd_eq_one : Nat.gcd e ((p - 1) * (q - 1) / Nat.gcd (p - 1) (q - 1)) = 1) : decrypt_rsa e p q (encrypt_rsa e p q m p_prime q_prime phi_coprime msg_bound) p_prime q_prime phi_coprime gcd_eq_one = m := by
    unfold encrypt_rsa
    unfold decrypt_rsa
    unfold mod_inverse
    -- have h : (mod_inverse e ((p - 1) * (q - 1) / Nat.gcd (p - 1) (q - 1)) gcd_eq_one) * e % m = 1 := by
      -- sorry
    have h1 (a b c d: Nat) (hc : c ≠ 0) : (((a ^ b) % c) ^ d) % c = (a ^ (b * d) % c) := by
      repeat rw [Nat.mod_def]
      by_cases h : c ∣ (a ^ b)
      ·
        have h1 : c * (a ^ b / c) = a^b := by exact Nat.mul_div_cancel' h
        rw[h1]
        simp
        by_cases h2 : d = 0
        · simp_all
        ·
          have h3 : 0 ^ d = 0 := by
            refine Nat.zero_pow_of_pos d ?h
            exact Nat.zero_lt_of_ne_zero h2
          rw[h3]
          simp_all
          have h4 : c * (a ^ (b * d) / c) = a ^ (b * d) := by
            have h4 : a ^ (b*d) = (a ^ b) ^ d := by
              exact Nat.pow_mul a b d
            have h5 : (a ^ b) ^ d = (a ^ b) ^ (d - 1) * (a ^ b) := by
              exact (Nat.pow_pred_mul (Nat.zero_lt_of_ne_zero h2)).symm
            rw[Nat.pow_mul, h5]
            have h6 : c ∣ a ^ b * (a ^ b) ^ (d - 1) := by
              unfold Dvd.dvd at h
              unfold Nat.instDvd at h
              simp at h
              unfold Dvd.dvd
              unfold Nat.instDvd
              simp
              cases h with
              | intro x hx =>
                rw[hx]
                refine Exists.intro ?intro.w ?intro.h
                exact x * (c * x) ^ (d - 1)
                exact Nat.mul_assoc c x ((c * x) ^ (d - 1))
            rw[Nat.mul_comm] at h6
            exact Nat.mul_div_cancel' h6
          rw[h4]
          simp
      · sorry







      have h : (a ^ b - c * (a ^ b / c)) ^ d = 0 := by
        have h : c * (a ^ b / c) = a ^ b := by
          refine Nat.mul_div_cancel' ?H
