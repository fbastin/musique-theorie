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
    \key g \major
    \omit Staff.TimeSignature
    \cadenzaOn
    \once \omit Accidental fis'1 \once \omit Accidental fis''1 f'!1 \once \omit Accidental f'1 \bar "|" \once \omit Accidental fis'1 fisis'!1
    \bar "|."
  }
  \addlyrics { \set ignoreMelismata = ##t "fa dièse" "fa dièse" "fa" "fa" "fa dièse" "fa double dièse" }
  \layout { \context { \Lyrics \override LyricSpace.minimum-distance = #2 } }
}
