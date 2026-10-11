\version "2.24.3"
%% Fichier produit par outils/generer_lecture.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new PianoStaff <<
    \new Staff = "haut" {
      \clef treble \omit Staff.TimeSignature \cadenzaOn
      c'1 \bar "||" s1 s1 s1 s1 c'1 d'1 e'1 f'1 g'1 \bar "|."
    }
    \new Staff = "bas" {
      \clef bass \omit Staff.TimeSignature \cadenzaOn
      c'1 \bar "||" f1 g1 a1 b1 s1 s1 s1 s1 s1 \bar "|."
    }
  >>
  \layout { }
}
