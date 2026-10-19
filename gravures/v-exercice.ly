\version "2.24.3"
%% Fichier produit par outils/generer_valeurs.py — ne pas modifier à la main.
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
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp \override TextScript.staff-padding = #3
      c''4._\markup \small 1 d''8 e''2 \bar "|" e''2~_\markup \small 2 e''8[ d''8] \bar "|" \tuplet 3/2 { c''8[_\markup \small 3 d''8 e''8] } f''4 \bar "|" g''8.[_\markup \small 4 f''16] r4 e''8 \bar "|" e''2.._\markup \small 5 \bar "|" \tuplet 6/4 { d''16[_\markup \small 6 e''16 f''16 g''16 f''16 e''16] } r4. d''8 \bar "|" r2_\markup \small 7 b'4~ b'8 \bar "|" \tuplet 4/3 { d''8[_\markup \small 8 c''8 b'8 a'8] } g'8 \bar "|" \tuplet 3/2 { a'4_\markup \small 9 b'4 c''4 } d''2 \bar "|" \tuplet 2/3 { e''8[_\markup \small 10 d''8] } c''4.
      \bar "|."
    }
  \layout {
     line-width = 170\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
