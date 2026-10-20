\version "2.24.3"
%% Fichier produit par outils/generer_tonalites.py — ne pas modifier à la main.
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
    \clef treble \key c \major \time 4/4
    \override TextScript.staff-padding = #3.5
    <c' e' g'>1_\markup \small \center-column { "do : I" } | <a' c'' e''>1_\markup \small \center-column { "do : VI" "sol : II" } | <d' fis' a'>1_\markup \small \center-column { "sol : V" } | <g' b' d''>1_\markup \small \center-column { "sol : I" }
    \bar "|."
  }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
