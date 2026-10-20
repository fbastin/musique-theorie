\version "2.24.3"
%% Fichier produit par outils/generer_mordants.py — ne pas modifier à la main.
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
      \clef treble \time 4/4
      \key c \major \afterGrace d''2\startTrillSpan { c''16[ d''16\stopTrillSpan] } c''2
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic \concat { "XVIII" \super "e" " s." } } {
      \clef treble \time 4/4 \autoBeamOff
      \key c \major e''32[ d''32 e''32 d''32 e''32 d''32 e''32 d''32] e''32[ d''32 e''32 d''32 e''32 d''32 c''32 d''32] c''2
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic \concat { "XIX" \super "e" " s." } } {
      \clef treble \time 4/4 \autoBeamOff
      \key c \major d''32[ e''32 d''32 e''32 d''32 e''32 d''32 e''32] d''32[ e''32 d''32 e''32 d''32 c''32 d''16] c''2
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
