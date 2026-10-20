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
    \once \omit Accidental g'1 gis'!1 ges'!1 gisis'!1 geses'!1 g'!1
    \bar "|."
  }
  \addlyrics { \set ignoreMelismata = ##t "sol" "sol dièse" "sol bémol" "sol double dièse" "sol double bémol" "sol" }
  \addlyrics { \set ignoreMelismata = ##t \override LyricText.font-size = #-2 \override LyricText.color = #(x11-color 'grey40) "" "" "" "sonne la" "sonne fa" "" }
  \layout { \context { \Lyrics \override LyricSpace.minimum-distance = #2 } }
}
