\version "2.24.3"
%% Fichier produit par outils/generer_mesure.py — ne pas modifier à la main.
\paper {
  indent = 0
  paper-width = 152\mm
  line-width = 150\mm
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
  \new Staff { \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature \override TextScript.staff-padding = #4
        \time 4/4 c''4 d''8[_\markup \small 1 e''8]~_\markup \small 2 e''8[ d''8] c''4 | r8 g'8_\markup \small 3 a'8[ b'8] c''2_\markup \small 4 | e''4 d''2_\markup \small 5 c''4 | r4 b'4_\markup \small 6 r8 d''8_\markup \small 7 c''4~_\markup \small 8 | c''2 b'4 c''4
        \bar "|."
      } }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
