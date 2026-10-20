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
    \clef treble
    
    \omit Staff.TimeSignature
    \cadenzaOn
    \once \omit Accidental g'1 fis'!1~ \bar "|" \once \omit Accidental fis'1 \once \omit Accidental e'1 \once \omit Accidental f'1
    \bar "|."
  }
  \addlyrics { \set ignoreMelismata = ##t "sol" "fa dièse" "fa dièse" "mi" "fa" }
  \layout { \context { \Lyrics \override LyricSpace.minimum-distance = #2 } }
}
