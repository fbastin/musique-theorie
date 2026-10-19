\version "2.24.3"
%% Fichier produit par outils/generer_interpretation.py — ne pas modifier à la main.
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
  \new StaffGroup <<
\new Staff \with { instrumentName = \markup \small \italic "écrit" } {
      \clef treble \time 2/4 
      c''4-._\markup \small \italic "staccato" e''4-. | c''4-!_\markup \small \italic "staccatissimo" e''4-! | c''4-.(_\markup \small \italic "portato" e''4-.) | c''4--_\markup \small \italic "tenuto" e''4--
      \bar "|."
    }
\new Staff \with { instrumentName = \markup \small \italic \center-column { "à peu près" "joué" } } {
      \clef treble \time 2/4 
      c''8 r8 e''8 r8 | c''16 r16 r8 e''16 r16 r8 | c''8. r16 e''8. r16 | c''4 e''4
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
