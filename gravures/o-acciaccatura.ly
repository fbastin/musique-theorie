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
  \new StaffGroup <<
    \new Staff \with { instrumentName = \markup \small \italic "écrit" } {
      \clef treble \time 2/4
      \key c \major \appoggiatura d''8 c''4 \acciaccatura d''8 c''4 | \acciaccatura d''8 c''2
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "joué" } {
      \clef treble \time 2/4 \autoBeamOff
      \key c \major \grace s8 d''8[ c''8] d''32[ c''8..] | d''32[ c''8..]~ c''4
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
