\version "2.24.3"
%% Fichier produit par outils/generer_ornements.py — ne pas modifier à la main.
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
  \new Staff  {
      \clef treble \time 3/4 \override TextScript.staff-padding = #4
      \key f \major \appoggiatura d''8 c''2._\markup \small 1 | a'2*1/2_\markup \small 2 s4\turn bes'4\mordent_\markup \small 3 | \acciaccatura a'8 g'4_\markup \small 4 c''4\turn_\markup \small 5 \appoggiatura g''8 f''4_\markup \small 6 | \afterGrace e''2\startTrillSpan_\markup \small 7 { d''16[ e''16\stopTrillSpan] } f''4
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
