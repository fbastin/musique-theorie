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
  \new Staff {
    \clef bass
    \omit Staff.TimeSignature
    \cadenzaOn
    c'1 b1 a1 g1 f1 e1 d1 c1 b,1 a,1 g,1 f,1 e,1 d,1 c,1
    \bar "|."
  }
  \addlyrics { do si la sol fa mi ré do si la sol fa mi ré do }
  \layout { }
}
